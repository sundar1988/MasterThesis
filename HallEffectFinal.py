##------------------------
##Import
##------------------------
import RPi.GPIO as GPIO
import time
##------------------------
##Set all GPIO
##------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
##----------
##GPIO assignment
##----------

HALL_SENSOR = 18
LED = 16
##--------
GPIO.setup (HALL_SENSOR,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)
##------------------------
##Initialization
##------------------------
counter=0
MaxCounter=10
        


def my_callback(channel):
    global counter
    global MaxCounter
    counter =counter+1
    print "count %d" %counter
    if MaxCounter > 0:
        MaxCounter=MaxCounter-1
        GPIO.output (LED,True)
        print "\n Street lamp ON" 

    else:
        GPIO.output (24,False)
        print "\n Street lamp OFF"
GPIO.add_event_detect(HALL_SENSOR, GPIO.BOTH, callback = my_callback, bouncetime=1000)
           
        
            
      
        

        
