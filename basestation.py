# -*- coding: utf-8 -*-
"""
base.py - This is the base program that is used to collect the readings
from the sensorboards in the house.  Each board has a unique MY address:

A - Masterbedroom
B - Basement
0 - Base 

The base station queries each unit by setting the DL address and then 
sending a # character.  The sensorboard responds with a message that 
contains the current readings along with the labels.  In order to keep
things simple, the readings are multiplied by ten and sent as ints.

The base looks for a complete message (> 50 bytes), if incomplete it queries
the board again.

Once the messages are read, the data is added to the sensordb database using
sqlite3. Then the base sleeps for 5 minutes before doing it again 
"""

import serial, time, os, sys
import sqlite3 as lite


ser = serial.Serial(port='/dev/ttyUSB0',timeout=2) 

data = {}

while True:
    # put in command mode
    ser.flush()
    time.sleep(1)
    ser.write('+++')
    time.sleep(2)
    
    #set DL address
    ser.flushInput()
    ser.write('ATDL A, ')
    time.sleep(3.2)
    ser.flushInput()
    
    msgComplete = False
    while not msgComplete:
        ser.flushInput()
        ser.write("#")
        s=ser.readline()
#        print "Board 1:", len(s)
        if len(s) > 50:
            msgComplete = True
    
    # Parse the message
    readings = s.strip().split(',')
    for reading in readings:
        name, value = reading.split(':')
        data[name] = float(value)/10
    
    # Read board B
    ser.flush()
    time.sleep(1)
    ser.write('+++')
    time.sleep(2)
    
    ser.flushInput()
    ser.write('ATDL B, ')
    
    time.sleep(3.2)
    ser.flushInput()
    
    msgComplete = False
    while not msgComplete:
        ser.flushInput()
        ser.write("#")
        s=ser.readline()
#        print "Board 2:", len(s)
        if len(s) > 50:
            msgComplete = True
            
    # Parse the message
    readings = s.strip().split(',')
    for reading in readings:
        name, value = reading.split(':')
        data[name] = float(value)/10
        
    
    # Insert the values into database
    names = "INSERT INTO readings (date, time"
    values = [time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S")]
    for item in data.keys():
        #print item, data[item]
        names = names + ", "+ item
        values.append(data[item])

    names = names + ") VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
    
    con = lite.connect('sensordb')
    with con:
        
        cur = con.cursor()

        cur.execute(names, values)


    time.sleep(300)
