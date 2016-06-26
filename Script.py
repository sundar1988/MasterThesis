# -*- coding: utf-8 -*-
##------------------------
##Import
##------------------------
import web
#import sys
import RPi.GPIO as GPIO
import time
import drivePWM # this module is design to set PWM 
#import pyfirmata
import time
#from Adafruit_I2C import Adafruit_I2C
#from time import sleep
#import math

##------------------------
##I2C device defination
##------------------------
##address = 0x49 #TSL2561
##i2c = Adafruit_I2C(address)
##control_on = 0x03
##control_off = 0x00

##------------------------
##Defination
##------------------------


##------------------------
##URL defination
##------------------------
urls = (
   '/','Root',"/root2","root2",'(/.+)','root1'
)
##------------------------
##Set all GPIO
##------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

HALL_SENSOR = 23 #RPi pin
ROTARY_ENCODER=25 #RPi pin

GPIO.setup (HALL_SENSOR,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ROTARY_ENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

##------------------------
##I2C Channel
##------------------------

FrontLampDown=0
FrontLampMid=1
FrontLampUp=2
LampRight=3
LampLeft=4
StreetLamp=5
CableCar=6

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
Script= web.application(urls, globals())

#render = web.template.render('template/')

##------------------------
##
##------------------------

class Root:
    def __init__ (self):
        self.hello = "hello world"
    		
    def GET(self):        
        INPUT= web.input(select="", setvalue="")
        command= str (INPUT.select)
        global deValue
        deValue = int (INPUT.setvalue)

        if command == "frontlampdown":
            import LuxPWMfld
            savedLux=LuxPWMfld.saveLux
            pwmFLD = LuxPWMfld.selectLux(deValue)# deValue is required Lux             
            drivePWM.select(0,pwmFLD)
            if pwmFLD !=0:
                return 'Front Down lamp ON, with pwm value:',pwmFLD,'Lux Range:',savedLux[0],'to',savedLux[256]
            else:
                return "Front Down lamp OFF"
        if command == "frontlampmid":
            import LuxPWMflm
            savedLux=LuxPWMflm.saveLux
            pwmFLM = LuxPWMflm.selectLux(deValue)# deValue is required Lux             
            drivePWM.select(1,pwmFLM)
            if pwmFLM !=0:
                return 'Front Mid lamp ON, with pwm value:',pwmFLM,'Lux Range:',savedLux[0],'to',savedLux[256]
            else:
                return "Front Mid lamp OFF"
        if command == "frontlampup":
            import LuxPWMflu
            savedLux=LuxPWMflu.saveLux
            pwmFLU = LuxPWMflu.selectLux(deValue)# deValue is required Lux             
            drivePWM.select(2,pwmFLU)
            if pwmFLU !=0:
                return 'Front UP lamp ON, with pwm value:',pwmFLU,'Lux Range:',savedLux[0],'to',savedLux[256]
            else:
                return "Front UP lamp OFF"
        if command == "lampright":
            import LuxPWMlr
            savedLux=LuxPWMlr.saveLux
            pwmLR = LuxPWMlr.selectLux(deValue)# deValue is required Lux             
            drivePWM.select(3,pwmLR)
            if pwmLR !=0:
                return 'Right Lamp ON, with pwm value:',pwmLR,'Lux Range:',savedLux[0],'to',savedLux[256]
            else:
                return "Right Lamp OFF"
        if command == "lampleft":
            import LuxPWMll
            savedLux=LuxPWMll.saveLux
            pwmLL = LuxPWMll.selectLux(deValue)# deValue is required Lux             
            drivePWM.select(4,pwmLL)
            if pwmLL !=0:
                return 'Left lamp ON, with pwm value:',pwmLL,'Lux Range:',savedLux[0],'to',savedLux[256]
            else:
                return "Left lamp OFF"
            
        if command == "streetlamp":          
            drivePWM.select(5,deValue)# here deValue is direct pulse (0..4096)
            
            if deValue !=0:
                return "Street Lamp ON,with PWM value %d" %deValue
            else:
                return "Street Lamp OFF"
##------------------------
##Cable Car
##-----------------------
         
       	# Hall sensor is used to detect the presence of the object
       	# add_event_detect function works on the multiple threading protocal
       	# MaxCounter is the required counter value inputed by user in web
       	# to give the value of 'MaxCounter' user must select ?turn=111
        if command == "cablecar":
            drivePWM.select(6,deValue)# here deValue is direct pulse (0..4096)
            def my_callback(channel):
                global counter
                global MaxCounter
                counter =counter+1
                #print "count %d" %counter
                if deValue != 0 and MaxCounter > 0:
                    MaxCounter=MaxCounter-1
                    drivePWM.select(6,deValue)
                    return "\n Cable Car running, with PWM speed %d" %deValue
            
                else:
                    drivePWM.select(6,0)
                    return "\n Cable Car STOP"
            GPIO.add_event_detect(HALL_SENSOR, GPIO.FALLING, callback = my_callback, bouncetime=300)
            return "\n Cable Car running, with PWM speed %d" %deValue
               
        # Input to the maximum counter
        if command == "setcounter":
            global MaxCounter
            MaxCounter= deValue-1
            GPIO.remove_event_detect (HALL_SENSOR)
            drivePWM.select(6,0)
            return "Maximum counter inputed: %d" %deValue
        else:
            return "No such device exist!! Type help."
        
        
        
        

class root1:
   
    def GET(self, command1):   
        command1=str (command1)
        
        # help section
        if command1 == "/help":
            import Help
            return Help.script()
                        
        # read counter value
        if command1 == "/getcountervalue":
            global counter
            return "counter value is %d" %counter

        # new approach for RPM measurement from rotary encoder      
	# this is based on the event detection (multiple threading process)
	# when this section is selected, the rpm count is being processed in the background
	# variable rpm is updated in each 5 second
	# updated variable 'rpm' is return to show the current RPM to the user via web

        if command1 == "/startrpmcounter":
            
            t0=time.time()
            rpmCount=-1
            
            def get_encoder_turn(channel):   
                global rpmCount
                rpmCount=rpmCount+1
                #print "rpm count %d"%rpmCount
                return rpmCount
            GPIO.add_event_detect(ROTARY_ENCODER, GPIO.BOTH, callback = get_encoder_turn)   	 
            x=0
            
            while True:              
                t1=time.time()
                          
                if t1-t0>=5:#each 5 sec
                    global rpm
                    global rpmCount
                    x=get_encoder_turn(ROTARY_ENCODER)# each 5 second it calls get_encoder_turn function
                    y=x
                    x=0
                    rpmCount=-1
                    rpm=(y/48)  #(y/48)*(60/5) --1 revolution is equal to 48 increment.
                            #(24 pulse per 360 degree)
                           
                   
                    #print "The motor RPM is:",rpm                   
                    t0=t1
            
	if command1 == "/getrpm":
            global rpm
            return "rpm: %f " %rpm
        if command1 == "/getspeed":
            global rpm
            speed = 2*3.14159*3*(float(rpm)/60)# 2*PI*radius in cm*rps (speed in cm/second)
            return "speed: %f" %speed
        if command1 == "/resetrpm":
	    global rpm
            rpm=0
            #GPIO.remove_event_detect (21)
            GPIO.remove_event_detect (ROTARY_ENCODER)
            return "RPM counter reseted"
       
        # reset counter
        if command1 == "/resetcounter":
            GPIO.remove_event_detect (23)
            global counter
            counter=0
            return "counter reseted"
	#RPM need not to be reseted
        
        if command1 == "/getlux":          
            import LuxSensor39
            LuxSensor39.enable()
            return LuxSensor39.getLight()
            LuxSensor39.disable()
        if command1 == "/stopcar":
            GPIO.remove_event_detect (HALL_SENSOR)
            drivePWM.select(6,0)
            return "Cable car stoped"
        
            
                                    
        if command1 == "/alldeviceoff":
            drivePWM.select(0,0)
            drivePWM.select(1,0)
            drivePWM.select(2,0)
            drivePWM.select(3,0)
            drivePWM.select(4,0)
            drivePWM.select(5,0)
            drivePWM.select(6,0)
           
            return "All Devices are set to zero"
        else:
            return "Wrong Selection.Type help!!"
        
        
if __name__ == '__main__':
    Script.run()

