# -*- coding: utf-8 -*-
"""
sensorboard.py

This script reads and logs the data from the propeller sensor board
The data comes in serially from the XBee connected to the computer

The sensorboard is outputing data at about 1Hz but we average and
log it only once every two minutes

"""

import serial,struct
import time

#Initialize some vars for our averages
Temp1Sum = 0.0
Temp2Sum = 0.0
Temp3Sum = 0.0
Temp4Sum = 0.0
count = 0.0

# Open the serial port connected to the XBee 9600,n,8,1
s_port = serial.Serial(9)

#Open a data file

while True:     # Loop forever
    s_port.flushInput()
    sdata = s_port.read(25)
    
    rdata = struct.unpack('<b h b b h b h b b h b b h b b h b b b',sdata)
    
    # unpack the data
    sensor1 = rdata[6:9]
    sensor2 = rdata[9:12]
    sensor3 = rdata[12:15]
    sensor4 = rdata[15:18]
    
    temp1 = int(sensor1[0]/2)-.25 + (sensor1[2]-sensor1[1])/float(sensor1[2])
    temp1 = temp1*1.8 + 32
    
    temp2 = int(sensor2[0]/2)-.25 + (sensor2[2]-sensor2[1])/float(sensor2[2])
    temp2 = temp2*1.8 + 32
    
    temp3 = int(sensor3[0]/2)-.25 + (sensor3[2]-sensor3[1])/float(sensor3[2])
    temp3 = temp3*1.8 + 32
    
    temp4 = int(sensor4[0]/2)-.25 + (sensor4[2]-sensor4[1])/float(sensor4[2])
    temp4 = temp4*1.8 + 32
    
    Temp1Sum += temp1
    Temp2Sum += temp2
    Temp3Sum += temp3
    Temp4Sum += temp4
    count += 1

    if count >= 20:
        temp1 = Temp1Sum/count
        temp2 = Temp2Sum / count
        temp3 = Temp3Sum / count
        temp4 = Temp4Sum / count
        
        outfile = open(time.strftime("%B%d_%Y")+'.log','a');
        outfile.write(time.strftime("%H:%M:%S"))
        outfile.write(' %5.2f   %5.2f   %5.2f   %5.2f\n' % (temp1, temp2, temp3, temp4))
        outfile.close
        count = 0
        Temp1Sum = Temp2Sum = Temp3Sum = Temp4Sum = 0.0
