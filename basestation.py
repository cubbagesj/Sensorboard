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

    # Create an HTML document with the current readings
    # do this by manually creating the html code
    # 

    curfile = open("webserver/index.html", "w")
    curfile.write('<!DOCTYPE HTML PUBLIC " -//W3C//DTD HTML 4.0 Transitional//EN">\n')
    curfile.write('<HTML> \n')
    curfile.write('<HEAD>\n')
    curfile.write('<META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=utf-8">\n')
    curfile.write('</HEAD>\n')
    curfile.write('<BODY LANG="en-US" DIR="LTR">\n')
    curfile.write('<P ALIGN=CENTER><FONT SIZE=5 STYLE="font-size: 20pt"><B>Current Conditions</B></FONT></P>\n')
    curfile.write('<P ALIGN=CENTER><B>')
    curfile.write('%s  %s'% (values[0], values[1]))
    curfile.write('</B></P>\n')
    curfile.write('<P ALIGN=CENTER><BR><BR></P>\n')
    for item in data.keys():
        curfile.write('<P ALIGN=LEFT> \n')
        curfile.write("%s %.2f \n" % (item, data[item]))
        curfile.write('</P>\n')
    curfile.write('</BODY>\n')
    curfile.write('</HTML>\n')

    curfile.close()

    time.sleep(300)
