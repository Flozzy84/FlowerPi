#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import the PySerial library and sleep from the time library
import serial
import time
from time import sleep
# Future use
import math
# Import plotly graph API
import plotly
py = plotly.plotly(username_or_email="Name", key="PWD")
# Import cPickle to manage a file with all data
import cPickle as pickle

# declare to variables, holding the com port we wish to talk to and the speed
port = '/dev/ttyAMA0'
baud = 9600

# open a serial connection using the variables above
ser = serial.Serial(port=port, baudrate=baud)

# wait for a moment before doing anything else
sleep(0.2)

# clear out the serial input buffer to ensure there are no old messages lying around
ser.flushInput()

# Minute to keep track in loops
minute = int(time.strftime("%M"))

# Create thre emty lists for mean value
reslist0 = []
reslist1 = []
reslist2 = []

# Logging
tm = time.strftime("%c")
print("Script started: {}".format(tm))

while minute < 55:
	# Loop 0
	# write a--A00READ-- out to the serial port
	# this will return the current ADC reading for Pin A0
	if minute in (0, 10, 20, 30, 40, 50):
		tm = time.strftime("%H:%M:%S")
		print("Trying to read A00 at: {}".format(tm))
		ser.write('a--A00READ--')
	
		# wait for a moment before doing anything else
		sleep(0.2)
	
		# loop until the serial buffer is empty
		while ser.inWaiting():
			# read a single character
			char = ser.read()
		
			# check we have the start of a LLAP message
			if char == 'a':
				# start building the full llap message by adding the 'a' we have
				llapMsg = 'a'
			
				# read in the next 11 characters form the serial buffer
				# into the llap message
				llapMsg += ser.read(11)
			
				# now we split the llap message apart into devID and data
				devID = llapMsg[1:3]
				data = llapMsg[3:]
			
				# check the devID is correct for our device
				# (WIK ships as -- be default)
				if devID == '--':
					# check to see if the message is about A00
					# if not we skip the section of code
					if data.startswith('A00'):
						# take just the last part of the message
						# strip the traling -'s
						# and convert to an int
						res = int(data[4:].strip('-'))
						print("Resistans A00 is: {}. At time: {}".format(res, tm))
						reslist0.append(res)
						print("Resistanslist A00 is: {}".format(reslist0))
						# send time do LCD to display
						hm = time.strftime("%H:%M")
						ser.write('a--{}----'.format(hm))
						print('a--{}----'.format(hm))
						sleep(0.2)
	# Loop 1
	# write a--A01READ-- out to the serial port
	# this will return the current ADC reading for Pin A1
	if minute in (1, 11, 21, 31, 41, 51):
		tm = time.strftime("%H:%M:%S")
		print("Trying to read A01 at: {}".format(tm))
		ser.write('a--A01READ--')
	
		# wait for a moment before doing anything else
		sleep(0.2)
	
		# loop until the serial buffer is empty
		while ser.inWaiting():
			# read a single character
			char = ser.read()
		
			# check we have the start of a LLAP message
			if char == 'a':
				# start building the full llap message by adding the 'a' we have
				llapMsg = 'a'
			
				# read in the next 11 characters form the serial buffer
				# into the llap message
				llapMsg += ser.read(11)
			
				# now we split the llap message apart into devID and data
				devID = llapMsg[1:3]
				data = llapMsg[3:]
			
				# check the devID is correct for our device
				# (WIK ships as -- be default)
				if devID == '--':
					# check to see if the message is about A01
					# if not we skip the section of code
					if data.startswith('A01'):
						# take just the last part of the message
						# strip the traling -'s
						# and convert to an int
						res = int(data[4:].strip('-'))
						print("Resistans A01 is: {}. At time: {}".format(res, tm))
						reslist1.append(res)
						print("Resistanslist A01 is: {}".format(reslist1))
						# send time do LCD to display
						hm = time.strftime("%H:%M")
						ser.write('a--{}----'.format(hm))
						print('a--{}----'.format(hm))
						sleep(0.2)
	# Loop 2
	# write a--A02READ-- out to the serial port
	# this will return the current ADC reading for Pin A2
	if minute in (2, 12, 22, 32, 42, 52):
		tm = time.strftime("%H:%M:%S")
		print("Trying to read A02 at: {}".format(tm))
		ser.write('a--A02READ--')
	
		# wait for a moment before doing anything else
		sleep(0.2)
	
		# loop until the serial buffer is empty
		while ser.inWaiting():
			# read a single character
			char = ser.read()
		
			# check we have the start of a LLAP message
			if char == 'a':
				# start building the full llap message by adding the 'a' we have
				llapMsg = 'a'
			
				# read in the next 11 characters form the serial buffer
				# into the llap message
				llapMsg += ser.read(11)
			
				# now we split the llap message apart into devID and data
				devID = llapMsg[1:3]
				data = llapMsg[3:]
			
				# check the devID is correct for our device
				# (WIK ships as -- be default)
				if devID == '--':
					# check to see if the message is about A02
					# if not we skip the section of code
					if data.startswith('A02'):
						# take just the last part of the message
						# strip the traling -'sprint('a--{}----'.format(hm))
						# and convert to an int
						res = int(data[4:].strip('-'))
						print("Resistans A02 is: {}. At time: {}".format(res, tm))
						reslist2.append(res)
						print("Resistanslist A02 is: {}".format(reslist2))
						# send time do LCD to display
						hm = time.strftime("%H:%M")
						ser.write('a--{}----'.format(hm))
						print('a--{}----'.format(hm))
						sleep(0.2)

	sleep(60)
	minute = int(time.strftime("%M"))

# Update lists and upload to plot.ly
print("Trying to calculate an upload result!")
# data A00
mean0 = sum(reslist0)/6
datalist0r = pickle.load(open('/home/pi/Py-Scripts/datafile0.p', 'rb'))
datalist0r.append(mean0)
pickle.dump(datalist0r[-240:], open('/home/pi/Py-Scripts/datafile0.p', 'wb'))

# data A01
mean1 = sum(reslist1)/6
datalist1r = pickle.load(open('/home/pi/Py-Scripts/datafile1.p', 'rb'))
datalist1r.append(mean1)
pickle.dump(datalist1r[-240:], open('/home/pi/Py-Scripts/datafile1.p', 'wb'))

# data A02
mean2 = sum(reslist2)/6
datalist2r = pickle.load(open('/home/pi/Py-Scripts/datafile2.p', 'rb'))
datalist2r.append(mean2)
pickle.dump(datalist2r[-240:], open('/home/pi/Py-Scripts/datafile2.p', 'wb'))

# time list
timelist = pickle.load(open('/home/pi/Py-Scripts/timelist.p', 'rb'))
timelist.append(time.strftime("%Y-%m-%d %H:%M:%S"))
pickle.dump(timelist[-240:], open('/home/pi/Py-Scripts/timelist.p', 'wb'))

# Upload to plotly
response = py.plot(timelist, datalist0r, timelist, datalist1r, timelist, datalist2r, filename='MoistGraph', fileopt='overwrite')
print(response)

tm = time.strftime("%H:%M:%S")
print("Fine Exit at: {}".format(tm))
# close the serial port
ser.close()
