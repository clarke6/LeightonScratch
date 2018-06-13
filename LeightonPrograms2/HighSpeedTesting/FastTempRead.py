#The goal of this program is to record the highest-possible resolution data
#using all temperature sensors and a serial read for each data entry. To collect
#data along with draw events, use the "FMtest" program to draw desired amounts
#of water while this program is already running. Data is written to a file named
#"FastTempRead.csv" and this file is overwritten if it already exists. Always
#rename or move data files that you want to keep before running the program
#again.

import RPi.GPIO as GPIO
from time import time, sleep
import os
import glob
import serial

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, timeout=1)
ser.readlines()

ser.write(b"\x08\x01\x00\x02\x0e\x01\xe2\x58") #Initial Heartbeat
ser.readline()
thb1= time()

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

#Create datafile
filename = 'FastTempRead.csv'
data = open(filename, 'w')
data.write('Capacity,Power,Sensor 1,Sensor 2,Sensor 3,Sensor 4,Sensor 5,Elapsed Seconds\n')
data.close

t1 = time()
while True:
    data = open(filename,'a')
    thb2 = time()
    if (thb2-thb1) > 240:
        ser.write(b"\x08\x01\x00\x02\x0e\x01\xe2\x58") #Refresh Heartbeat
        ser.readline()
        thb1 = time()
        print('\nHeartbeat sent at %.2f sec.\n' %t)
    ser.write(b"\x08\x02\x00\x02\x06\x00\xf6\x4c") #Commodity request
    comm = ser.readline()
    comm = comm.encode('hex')
    P = str(int(comm[20:32],16))
    E = str(int(comm[84:96],16)) 
    data.write(E + ',' + P + ',')
    for Sensor in Sensor_files:
        data.write(str(read_temp(Sensor))+',')
    t2 = time()
    t = t2-t1
    data.write(str(t)+'\n')
    data.close
    
    
        
