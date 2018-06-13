import os
import glob
from time import time, sleep
import RPi.GPIO as GPIO
import csv
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
FMPIN = 6    #flow meter GPIO pin
VPIN = 12    #valve GPIO pin
HEPIN = 25   #heating element pin
TSPIN = 23   #temperature sensor pin
GPIO.setup(FMPIN, GPIO.IN, GPIO.PUD_UP) #setup flow meter pin as input
GPIO.setup(VPIN, GPIO.OUT, initial=GPIO.LOW)    #setup valve pin as output
GPIO.add_event_detect(FMPIN, GPIO.RISING)   #add rising edge detection
GPIO.setup(HEPIN, GPIO.OUT, initial=GPIO.LOW)  #setup heating element pin as output
GPIO.setup(TSPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #setup temp. sensor pin as input

#Initialize temperature sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-00043e9dc3ff')[0]
device_file = device_folder + '/w1_slave'

#Define functions for reading from temperature sensor
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
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
    while volume < target:  #keep valve open until desired volume has passed
        if GPIO.event_detected(FMPIN):
            numPulses += 1    #Count pulses from flow meter
            volume = float(numPulses) / 476    #Calculate volume
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

#Create file for temperature sensor data
PATH = 'Waterheater_Data.csv'
if os.path.isfile(PATH):
    print('A temperature data log already exists and will be overwritten.')
else:
    print('No temperature data log exists. A new one will be created')
data = open('Waterheater_Data.csv', 'w')
data.write('Time, Temperature\n')
data.close()

#Initialize plot figure
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

#Define function to animate plot
def animate(i):
    pullData = open('Waterheater_Data.csv','r').read()
    dataArray = pullData.split('\n')
    temps = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            if x[0].isdigit():
                temps.append(float(y))
        ax1.clear()
        ax1.plot(temps)


state = 0   #Variable to mark heating element state (0 is off)
#Enter main program loop
while True:
    now = datetime.now()    #Update time
    new_row = str() #Initialize string for new data row

    #Read temperature sensor, and adjust heating element if too hot or cold
    temp = read_temp()
    if temp > 120 and state == 1:
        GPIO.output(HEPIN, GPIO.LOW)
        state = 0
        print('Temperature has exceeded 120 degrees - turning off heating element.')
    elif temp < 118 and state == 0:
        GPIO.output(HEPIN, GPIO.HIGH)
        state = 1
        print('Temperature is below 118 degrees - turning on heating element.')

    #Log data every 10 minutes
    if now.minute % 1 == 0 and now.second == 0:
        new_row = new_row + str(now.hour) + ':' + str(now.minute) + ',' + str(temp)
        data = open('Waterheater_Data.csv', 'a')
        data.write(new_row + '\n')
        data.close
        print('Logging data: %.2f degrees Fahrenheit at %g:%g' % (temp,now.hour,now.minute))
        sleep(1)
    
    #Draw water at the start of each hour
    for i in range(len(hours)):
        if hours[i] == now.hour and now.minute == 0 and now.second < 2:
            draw_water(gallons[i])  #Draw scheduled volume for current hour
            sleep(2)    #Wait two seconds to prevent draw_water call from repeating

    ani = animation.FuncAnimation(fig,animate, interval=1000)
    plt.ion()
    plt.show()
