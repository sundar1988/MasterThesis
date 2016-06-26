#!/usr/bin/env python2.7
# This script is to deal with the interrupts with Python on Raspberry Pi.
# Threaded callback is introduced here.
# Reference: sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# Author : Sundar Shrestha 
# Date : 12 June, 2014

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings (False)

# GPIO 23,24 & 25 set up as inputs. One pulled up, the other down.
# 23 will go to GND when button pressed and 24 will go to 3V3 (3.3V)
# this enables us to demonstrate both rising and falling edge detection
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(25, GPIO.IN)
GPIO.setup(18, GPIO.OUT)

var=1
counter=0
# now we'll define the threaded callback function
# this will run in another thread when our event is detected
def my_callback(channel):
    global counter
    counter =counter+1
    print "count=%d" %counter
    print "Rising Edge Detected on pin 24"
    if counter <=4 and counter>=1:
	#GPIO.output(18,True)
	run_motor()
        print "LED ON"
    else:
	GPIO.output(18,False)
	print "LED OFF"
    if counter ==7:
	counter=0
def run_motor():
    GPIO.output(18,True)

def my_callback1(channel):
    global counter
    counter =counter+1
    print "count=%d" %counter
    print "Hall effect detection"
    if counter <=4 and counter>=1:
	
        run_motor()
	print "LED ON"
    else:
	GPIO.output(18,False)
	print "LED OFF"
    if counter ==7:
	counter=0

# The GPIO.add_event_detect() line below set things up so that
# when a rising edge is detected on port 24, regardless of whatever 
# else is happening in the program, the function "my_callback" will be run
# It will happen even while the program is waiting for
# a falling edge on the other button.
# bouncetime in millisecond. ignore the further edges for given millisecond.

GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback, bouncetime=10)
GPIO.add_event_detect(25, GPIO.BOTH, callback=my_callback1, bouncetime=1000)

try:
    print "Waiting for falling edge on port 23"
    GPIO.wait_for_edge(23, GPIO.FALLING)
    print "Falling edge detected." 

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
