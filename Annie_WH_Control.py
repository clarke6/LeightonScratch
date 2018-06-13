import os
import glob
from time import time, sleep
import RPi.GPIO as GPIO
import csv
import pandas as pd
from datetime import datetime

#Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
FMPIN = 6    #flow meter GPIO pin
VPIN = 17    #valve GPIO pin
HEPIN = 16   #heating element pin
TSPIN = 23   #temperature sensor pin
GPIO.setup(FMPIN, GPIO.IN, GPIO.PUD_UP) #setup flow meter pin as input
GPIO.setup(VPIN, GPIO.OUT, initial=GPIO.LOW)    #setup valve pin as output
GPIO.add_event_detect(FMPIN, GPIO.RISING)   #add rising edge detection
GPIO.setup(HEPIN, GPIO.OUT, initial=GPIO.LOW)  #setup heating element pin as output
GPIO.setup(TSPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #setup temp. sensor pin as input

#Read csv to create sensor ID array
sensorFile = open('Sensor_List.csv', 'r').read()
sensors = sensorFile.split('\n')
sensors.remove(sensors[0]) # Remove header
sensIDs = [] # Initialize array of Sensor IDs
for eachLine in sensors:
    if len(eachLine) > 1:
        eachLine = eachLine.split(',')
        sensIDs.append(eachLine[1])

#Initialize temperature sensors and create array of file locations
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
Sensor_files = []
for ID in sensIDs:
    device_folder = glob.glob(base_dir + ID)[0]
    Sensor_files.append(device_folder + '/w1_slave')


#Define functions for reading from temperature sensor
def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

#Define function to draw water
def draw_water(target):
    if target == 0:
        print('No draw for this hour')
        return()
    print ('Drawing %.2f gallon(s).' % target)
    volume = 0
    numPulses = 0
    GPIO.output(VPIN, GPIO.HIGH)    #open valve
    start_time = time()
    while volume < target:  #keep valve open until desired volume has passed
        if GPIO.event_detected(FMPIN):
            numPulses += 1    #Count pulses from flow meter
            volume = float(numPulses) / 458.8    #Calculate volume
        run_time = time()
        elapsed_time = run_time - start_time
        if elapsed_time > 180:
            print ('Timeout Error.')
            break
    GPIO.output(VPIN, GPIO.LOW) #close valve
    print ('Volume drawn: %.2f gallon(s).' % volume)

#Read csv file with daily usage profile (one column for hours, one for gallons)
dp = pd.read_csv('DailyProfile.csv')
hours = []
gallons = []
row = 0
while row < len(dp):
    hours.append(dp.get_value(row,'Hour '))
    gallons.append(dp.get_value(row,'gallons'))
    row += 1

state = 0   #Variable to mark heating element state (0 is off)
#Enter main program loop
while True:
    now = datetime.now()    #Update date/time
    filename = 'WH_Data_' + str(now.month) + '-' + str(now.day) + '-' + str(now.year) + '.csv'
    if not os.path.isfile(filename):    #Create new datafile if there isn't one for this date
        data = open(filename, 'w')
        data.write('Time,Sensor 1,Sensor 2,Sensor 3,Sensor 4\n')
        data.close
        print('Creating new data file for ' + str(now.month) + '-' + str(now.day) + '-' + str(now.year))
    
    #Read middle temperature sensor, and adjust heating element if too hot or cold
    temp = read_temp(Sensor_files[1])
    if temp > 120 and state == 1:
        GPIO.output(HEPIN, GPIO.LOW)
        state = 0
        print('Temperature has exceeded 120 degrees - turning off heating element.')
    elif temp < 118 and state == 0:
        GPIO.output(HEPIN, GPIO.HIGH)
        state = 1
        print('Temperature is below 118 degrees - turning on heating element.')

    #Log data every 2 minutes
    if now.minute % 2  == 0 and now.second < 2:
        data = open(filename, 'a')
        data.write(datetime.strftime(now,'%H:%M'))
        for eachSensor in Sensor_files:
            data.write(',' + str(read_temp(eachSensor)))
        data.write('\n')
        data.close
        print('Logging Temperature data.')
    
    #Draw water at the start of each hour
    for i in range(len(hours)):
        if hours[i] == now.hour and now.minute == 0 and now.second < 10:
            draw_water(gallons[i])  #Draw scheduled volume for current hour
            sleep(10)    #Wait 10 seconds to prevent draw_water call from repeating
