#-*- coding: utf-8 -*-
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings(False)
HALL_SENSOR = 18 # Hall sensor connected to GPIO 18
GPIO.setup (HALL_SENSOR,GPIO.IN) # Setup the GPIO pin connected to the Hall Sensor to read as input
global count
count=0

currentState=0
preState=0
requiredCount=4

# Main program loop
while True:
    hallActive = False
    if (GPIO.input(HALL_SENSOR) == False):                
        currentState=1
        if (currentState==1 and preState==1):
            count=count+1
            print "count %d" %count
            preState=0
            sleep(1)
            if count==requiredCount:                
                print "Cable Car complete %d rotation" %count
                count=0
    else:                 
        preState =1



