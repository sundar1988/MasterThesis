# -*- coding: utf-8 -*-
##------------------------
##Import
##------------------------
import web
#import sys
import RPi.GPIO as GPIO
import time
#from Adafruit_I2C import Adafruit_I2C
#from time import sleep
#import math
#import flash
##------------------------
##I2C device defination
##------------------------
##address = 0x49 #TSL2561
##i2c = Adafruit_I2C(address)
##control_on = 0x03
##control_off = 0x00
##------------------------
##URL defination
##------------------------
urls = (
   '/','root', '(/.+)', 'root1'
)
##------------------------
##Set all GPIO
##------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
##----------
#input_A = 25
#input_B = 21
HALL_SENSOR = 23
ROTARY_ENCODER=25
#GPIO.setup(input_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(input_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#old_a = True
#old_b = True
rpm=0

t0=time.time()
##--------
GPIO.setup(18,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup (HALL_SENSOR,GPIO.IN)
GPIO.setup(ROTARY_ENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#pwmMotor=GPIO.PWM(18,500)
pwmLight=GPIO.PWM(17,500)
pwmLight1=GPIO.PWM(18,500)
##------------------------
##Initialization
##------------------------
counter=0
MaxCounter=1000
rpmCount=-1
rpm=0

##------------------------
## URL handling
##------------------------
app = web.application(urls, globals())

#render = web.template.render('template/')

##------------------------
##
##------------------------

class root:
    def __init__ (self):
        self.hello = "hello world"
    		
    def GET(self):        
        INPUT= web.input(turn="", value="")
        command= str (INPUT.turn)
        global deValue
        deValue = int (INPUT.value)
        
       	# Hall sensor is used to detect the presence of the object
       	# add_event_detect function works on the multiple threading protocal
       	# MaxCounter is the required counter value inputed by user in web
       	# to give the value of 'MaxCounter' user must select ?turn=111
        if command == "1":
            def my_callback(channel):
                global counter
                global MaxCounter
                counter =counter+1
                print "count %d" %counter
                if deValue != 0 and MaxCounter > 0:
                    MaxCounter=MaxCounter-1
                    pwmLight.start(deValue)
                    print "\n Street lamp ON, with brightness %d" %deValue
            
                else:
                    pwmLight.start(0)
                    print "\n Street lamp OFF"
            GPIO.add_event_detect(23, GPIO.BOTH, callback = my_callback, bouncetime=1000)
               
        # Input to the maximum counter
        if command == "111":
            global MaxCounter
            MaxCounter= deValue
            GPIO.remove_event_detect (23)
            pwmLight.start(0)
            return "Maximum counter inputed: %d" %deValue
        
        if command == "22":			
            return "Welcome"
                   
        if command == "2":         
            GPIO.output (24,True)
            return "led 2 ON and command inputed is %s" %command
        
        if command == "3":          
            pwmMotor.start(deValue)            
            if deValue !=0:
                return "Motor running, with PWM value %d" %deValue
            else:
                return "Motor OFF"
        if command == "44":
            import LuxPWMselfReading
            pwmValue = LuxPWMselfReading.selectLux(deValue)             
            pwmLight.start(pwmValue)
            if pwmValue !=0:
                return "Street lamp ON, with pwm value %f" %pwmValue
            else:
                return "Street lamp OFF"
        if command == "454":
            import LuxPWMselfReading
            pwmValue = LuxPWMselfReading.selectLux(deValue)             
            pwmLight1.start(pwmValue)
            if pwmValue !=0:
                return "Street lamp ON, with pwm value %f" %pwmValue
            else:
                return "Street lamp OFF"
            
        # new approach for RPM measurement from rotary encoder      
	# this is based on the event detection (multiple threading process)
	# when this section is selected, the rpm count is being processed in the background
	# variable rpm is updated in each 5 second
	# updated variable 'rpm' is return to show the current RPM to the user via web

        if command == "5":            
            t0=time.time()
            rpmCount=-1
            def get_encoder_turn(channel):   
                global rpmCount
                rpmCount=rpmCount+1
                #print "rpm count %d"%rpmCount
                return rpmCount
	    GPIO.add_event_detect(25, GPIO.BOTH, callback = get_encoder_turn)	 
            x=0
            while True:              
                t1=time.time()
                          
                if t1-t0>=5:#each 5 sec
                    global rpm
                    global rpmCount
                    x=get_encoder_turn(25)# each 5 second it calls get_encoder_turn function
                    y=x
                    x=0
                    rpmCount=-1
                    rpm=y/4 #(y/48)*(60/5) --1 revolution is equal to 48 increment.
                            #(24 pulse per 360 degree)
                   
                    #print "The motor RPM is:",rpm                   
                    t0=t1
        

 
##------------------------
##Reset all GPIO
##-----------------------
        
        if command == "112":
            #GPIO.output(18,False)
            #GPIO.output(23,False)
            GPIO.output(24,False)
            #GPIO.output(17,False)
            
            return "All pin except pwm are reseted--please start again"
			
class root1:
   
    def GET(self, command1):   
        command1=str (command1)
       
        # read counter value
        if command1 == "/countervalue":
            global counter
            return "counter value is %d" %counter
	if command1 == "/rpm":
            global rpm
            return "rpm: %d" %rpm
       
        # reset counter
        if command1 == "/resetcounter":
            GPIO.remove_event_detect (23)
            global counter
            counter=0
            return "counter reseted"
	#RPM need not to be reseted
        if command1 == "/resetrpm":
	    global rpm
            rpm=0
            GPIO.remove_event_detect (21)
            GPIO.remove_event_detect (25)
            return "RPM counter reseted"
        if command1 == "/light":          
            import tsltry
            return tsltry.getLight()
            print lux
        
        
if __name__ == '__main__':
    app.run()

