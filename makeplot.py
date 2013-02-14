#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


import sqlite3 as lite
import sys

con = lite.connect('sensordb')


hours = mdates.HourLocator(interval=4)
minutes = mdates.MinuteLocator()

daysFmt = mdates.DateFormatter('%H:%M')

with con:

    # Get data from the past week
    delta = datetime.timedelta(2)
    past = datetime.datetime.now() - delta

    symbol = past.strftime("%Y-%m-%d")

    t = (symbol,)

    cur = con.cursor()
    cur.execute('SELECT date,time, humidity from readings where date>?', t)
     
    data = cur.fetchall()

    xdata = []
    ydata = []
    
    for row in data:
        xdata.append(datetime.datetime.strptime(row[0]+' '+row[1],"%Y-%m-%d %H:%M:%S"))
        ydata.append(row[2]) 

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(xdata, ydata)
    fig.autofmt_xdate()
 
    ax.set_ylabel('Humdity (%)')
    ax.set_xlabel('Time')
    ax.set_title('Humidity - last 48 hrs')
   
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(daysFmt)
    #ax.xaxis.set_minor_locator(minutes)

 

    plt.grid('on')
    plt.savefig('./static/humidity.png')
#    plt.show()

