Sensorboard
===========

Simple code to monitor a network of temperature sensors that are connected to the computer through
an XBee wireless network.

The program queries each remote XBee to get the latest temperatures and then enters the data into
a sqlite3 database

Consists of three main programs:

basestation.py: Gets the temperature readings from the XBee network and logs to database

sensor-site.py: Runs a Flask based website to display data

makeplots.py: queries database and makes some plots for display on webpage
