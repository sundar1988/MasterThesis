#!/usr/bin/python
## Date:        12.08.2014
## Author:      Sundar Shrestha
## Refrence:    Adafruit servo PWM code

##------------Overview-------------------------------------------------
# select PWM servo driver as address 0x40.
# function select is created to choose channel of driver and pulse.
# total channel 0--15
# min pulse = 0 and max pulse = 4096
##---------------------------------------------------------------------

from Adafruit_PWM_Servo_Driver import PWM
import time

pwm = PWM(0x40, debug=True)# Initialise the PWM device using the default address

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 50                       # 50 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)
  print "%d pulse"%pulse

pwm.setPWMFreq(50)# Set frequency to 50 Hz

def select(channel,pulse):
    pwm.setPWM (channel,0,pulse)# start from 0 always

       
 
		     
