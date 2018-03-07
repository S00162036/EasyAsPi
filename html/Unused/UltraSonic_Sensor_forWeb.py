#!../../usr/bin/env python

from gpiozero import DistanceSensor
import time

ultrasonic = DistanceSensor( echo = 17, trigger = 4)

cDist = 0
tempDist = 0
while True:
	for i in range(10):
		cDist = cDist + ultrasonic.distance
		time.sleep(.05)
	cDist = cDist/10  # Get the average of the 10 distances
	time.sleep(.1)
	tempDist = cDist
	if tempDist == cDist:
		output = round(cDist*100,3)
		forJSONtesting = output / 20
		text_file = open("indexOld.html", "w") #File being used as a prototyping database... don't know how we'll move onto cloud?
		text_file.write('{ "coinCount": "' + str(output) + '" , "twoEuroCount": "' + str(round(forJSONtesting,2)) + '" }')
		text_file.close()
		
	