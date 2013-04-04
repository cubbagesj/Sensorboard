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

# Open the data base 
con = lite.connect('/home/pi/Sensorboard/sensordb')

# Setup the date label formatting
hours = mdates.HourLocator(interval=4)
minutes = mdates.MinuteLocator()

daysFmt = mdates.DateFormatter('%H:%M')

with con:
    con.row_factory = lite.Row
 
    # Get  data from the past 2 days
    delta = datetime.timedelta(4)
    past = datetime.datetime.now() - delta

    symbol = past.strftime("%Y-%m-%d")

    t = (symbol,)

    cur = con.cursor()
    cur.execute('SELECT * from readings where date>?', t)
    
    # get all of the data into a big array
    data = cur.fetchall()

    # now try to make multiple plots

    plots = ["MasterBR", "Outside", "Basement", "Humidity"]
    #plots = ["MasterBR"]

    for plot in plots:

        xdata = []
        ydata = []
     
        for row in data:
            xdata.append(datetime.datetime.strptime(row["date"]+' '+row["time"],"%Y-%m-%d %H:%M:%S"))
            ydata.append(row[plot]) 

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(xdata, ydata)
        fig.autofmt_xdate()
 
        ax.set_ylabel(plot)
        ax.set_xlabel('Time')
        ax.set_title(plot+' - last 48 hrs')
   
        ax.xaxis.set_major_locator(hours)
        ax.xaxis.set_major_formatter(daysFmt)
    #ax.xaxis.set_minor_locator(minutes)

 

        plt.grid('on')
        plt.savefig('/home/pi/Sensorboard/static/'+plot+'.png')


