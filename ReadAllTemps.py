import os
import glob
from time import time, sleep
import RPi.GPIO as GPIO
import csv
import pandas as pd
from datetime import datetime

#Read csv to create sensor ID array
sensorFile = open('Sensor_List.csv', 'r').read()
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


t1=time()
temps=[]
for sensor in Sensor_files:
    temps.append(read_temp(sensor))
t2=time()
print t2-t1
print temps
    
    
