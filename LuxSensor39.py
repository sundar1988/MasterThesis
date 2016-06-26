# -*- coding: utf-8 -*-
#!/usr/bin/python
## Date:        12.08.2014
## Author:      Sundar Shrestha
## Refrence:    datasheet of TSL2561

##------------Overview-------------------------------------------------
# select TSL2561 as I2C address 0x39.
# function getLight reads IR and ambient light and convert into Lux.
##---------------------------------------------------------------------

from Adafruit_I2C import Adafruit_I2C
from time import sleep
import sys
import math
address = 0x39
i2c = Adafruit_I2C(address)
control_on = 0x03
control_off = 0x00

def enable():
    print "enabling"
    i2c.write8(0x80, control_on)

def disable():
    print "disabling"
    i2c.write8(0x80, control_off)
def getLight():
    IR = i2c.readU16(0xAE)
    ambient = i2c.readU16(0xAC)
      
    if ambient >=65535:
        print "max ambient"

    if (ambient <=0 or IR<=0):      
        IR=0
        ambient=1
    ratio =  IR /float(ambient)
    if ((ratio >= 0) & (ratio <= 0.52)):
        lux = (0.0315 * ambient) - (0.0593 * ambient * (ratio**1.4))
    elif (0.52<ratio <= 0.65):
        lux = (0.0229 * ambient) - (0.0291 * IR)
    elif (0.65<ratio <= 0.80):
        lux = (0.0157 * ambient) - (0.018 * IR)
    elif (0.80<ratio <= 1.3):
        lux = (0.00338 * ambient) - (0.0026 * IR)
    elif (ratio > 1.3):
        lux = 0
    return lux
    #print lux
##enable()
##sleep(2)
##while True:
##    #enable()
##    #sleep(0.1)
##    getLight()
##    sleep(1)
##    #disable()
###sleep(2)
  
