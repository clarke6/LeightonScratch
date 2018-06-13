#This is just a template for creating a serial object using the USB adapter

import time
import serial

#enter ls -l /dev in terminal to see name of USB port
ser = serial.Serial(port='/dev/ttyUSB1', baudrate=19200, timeout=1)



