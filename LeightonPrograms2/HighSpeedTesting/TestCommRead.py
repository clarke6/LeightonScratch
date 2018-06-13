#This program was altered specifically to measure energy capacity during several
#draw events. It is not really useful by itself, but may be used as a reference
#for how to combine temperature and energy capacity reads in a control program.

from datetime import datetime
from numpy.random import normal
from numpy import zeros, savetxt, loadtxt
import random
import RPi.GPIO as GPIO
from time import time, sleep
import os
import glob
import serial

#Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
FMPIN = 6    #flow meter GPIO pin
VPIN = 17    #valve GPIO pin
GPIO.setup(FMPIN, GPIO.IN, GPIO.PUD_UP) #setup flow meter pin as input
GPIO.setup(VPIN, GPIO.OUT, initial=GPIO.LOW)    #setup valve pin as output
GPIO.add_event_detect(FMPIN, GPIO.RISING)   #add rising edge detection

#Read csv to create sensor ID array
sensorFile = open('sensorID.csv', 'r').read()
sensors = sensorFile.split('\n')
sensors.remove(sensors[0]) # Remove header
sensIDs = [] # Initialize array of Sensor IDs
for eachLine in sensors:
    if len(eachLine) > 1:
        eachLine = eachLine.split(',')
        sensIDs.append(eachLine[1])

#Initialize temperature sensors
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

def generate_schedule():
    events = zeros((24,60))
    hourlySums = zeros(24)

    for hour in range(24):
        if hour < 6 or hour > 22:
            numEvents = int(normal(5,2))
            drawSize = 0.2
            drawSD = 0.05
        elif hour >= 5 and hour < 12:
            numEvents = int(normal(10,5))
            drawSize = 0.75
            drawSD = 0.5
        elif hour >=12 and hour < 17:
            numEvents = int(normal(7,2))
            drawSize = 0.25
            drawSD = 0.1
        elif hour >=17 and hour < 22:
            numEvents = int(normal(15,5))
            drawSize = 0.5
            drawSD = 0.3
        if numEvents > 0:
            minutes = random.sample(range(60),numEvents)
        else:
            numEvents = 0

        for event in range(numEvents):
            eventSize = normal(drawSize,drawSD)
            if eventSize > 0:
                events[hour][minutes[event]] = eventSize

        hourlySums[hour] = sum(events[hour])
    return events,hourlySums

#Define function to draw water
def draw_water(target):
    if target <= 0:
        return()
    print ('Drawing %.2f gallon(s).' % target)
    volume = 0
    numPulses = 0
    start_time = time()
    GPIO.output(VPIN, GPIO.HIGH)    #open valve
    while volume < target:  #keep valve open until desired volume has passed
        if GPIO.event_detected(FMPIN):
            numPulses += 1    #Count pulses from flow meter
            volume = float(numPulses) / 476    #Calculate volume
        run_time = time()
        elapsed_time = run_time - start_time
        if elapsed_time > 180:
            print('Timeout Error.')
            break
    GPIO.output(VPIN, GPIO.LOW) #close valve
    print ('Volume drawn: %.2f gallon(s).' % volume)

#Draw volumes
events = [0,0,0,0,0]
hours = [15,16,17,18,19]

#Create datafile
now = datetime.now()
filename = 'Test_Data_' + str(now.month) + '-' + str(now.day) + '-' + str(now.year) + '.csv'
data = open(filename, 'w')
data.write('Time,Sensor 1,Sensor 2,Sensor 3,Sensor 4,Sensor 5,Present Capacity\n')
data.close

#Create serial object, empty buffer
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, timeout=1)
ser.readlines()

#Enter main program loop
while True:
    now = datetime.now()    #Update date/time

    #Log data every 2 minutes, send heartbeat
    if now.minute % 2  == 0 and now.second < 3:
        ser.write(b"\x08\x01\x00\x02\x0e\x01\xe2\x58") #Confirm connection
        ser.readline()
        data = open(filename, 'a')
        data.write(datetime.strftime(now,'%H:%M'))
        for eachSensor in Sensor_files:
            data.write(',' + str(read_temp(eachSensor)))
        ser.write(b"\x08\x02\x00\x02\x06\x00\xf6\x4c") #Commodity read
        Commdata = ser.readline()
        Commdata = Commdata.encode('hex')
        Capacity = str(int(Commdata[84:96],16))
        data.write(',' + Capacity)
        data.write('\n')
        data.close
        print('Logging Temperature and capacity data.')

    #Draw specified volumes at corresponding times
    for i in range(len(hours)):
        if now.hour == hours[i] and now.minute == 0 and now.second<10:
            draw_water(events[i])
            sleep(10) #Wait to prevent draw_water call from being repeated
    sleep(1)
