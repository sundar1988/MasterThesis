# Written on : 17.06.2014
# Author : Sundar Shrestha
# This script is written to grab RPM value via Rotary Encoder
# Only one GPIO pin is used
# Based on multiple threading
# this script can be run in the background. This writes the rpm value in
# in external file say 'workfile.txt'.That value can be extracted from the
# main python file to get the value from web.

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
global rpm
rpm=0
t0=time.time()
rpmCount=-1

def get_encoder_turn(channel):   
    global rpmCount
    rpmCount=rpmCount+1
    return rpmCount
GPIO.add_event_detect(25, GPIO.BOTH, callback = get_encoder_turn)

x=0

while True:     
    t1=time.time()             
    if t1-t0>=5:#each 5 sec
        global rpm 
        x=get_encoder_turn(25)# each 5 second it calls gt_encoder_turn function
        y=x
        x=0
        rpmCount=-1
        rpm=y/3.416 #(y/41)*(60/5) --1 revolution is equal to 41 increment.

        print "The motor RPM is:",rpm
        rpm=str (rpm)
        f=open ('workfile.txt', 'w')
        f.write(rpm)
        f.close()
        #print"\n"
        #print ("10sec")
        t0=t1



