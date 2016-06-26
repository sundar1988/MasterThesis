#!/usr/bin/python
# Code sourced from AdaFruit discussion board: https://www.adafruit.com/forums/viewtopic.php?f=8&t=34922


import sys
# Not needed here. Thanks to https://github.com/mackstann for highlighting this.
import smbus
import time
from time import sleep
from Adafruit_I2C import Adafruit_I2C


### Written for Python 2 <-!!!
### Big thanks to bryand, who wrote the code that I borrowed heavily from/was inspired by


class TSL2561:
    i2c = None

    def __init__(self, address=0x49, debug=0, pause=0.8):
        self.i2c = Adafruit_I2C(address)
        self.address = address
        self.pause = pause
        self.debug = debug
        self.gain = 0 # no gain preselected
        self.i2c.write8(0x80, 0x03)     # enable the device


    def setGain(self,gain=1):
        """ Set the gain """
        if (gain != self.gain):
            if (gain==1):
                self.i2c.write8(0x81, 0x08)     # set gain = 1X and timing = 402 mSec
                if (self.debug):
                    print "Setting low gain"
            else:
                self.i2c.write8(0x81, 0x18)     # set gain = 16X and timing = 402 mSec
                if (self.debug):
                    print "Setting high gain"
            self.gain=gain;                     # safe gain for calculation
            time.sleep(self.pause)              # pause for integration (self.pause must be bigger than integration time)


    def readWord(self, reg):
        """Reads a word from the I2C device"""
        try:
            wordval = self.i2c.readU16(reg)
            newval = self.i2c.reverseByteOrder(wordval)
            if (self.debug):
                print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, wordval & 0xFFFF, reg))
            return newval
        except IOError:
            print("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1


    def readFull(self, reg=0x8C):
        """Reads visible+IR diode from the I2C device"""
        return self.readWord(reg);

    def readIR(self, reg=0x8E):
        """Reads IR only diode from the I2C device"""
        return self.readWord(reg);

    def readLux(self, gain = 0):
        """Grabs a lux reading either with autoranging (gain=0) or with a specified gain (1, 16)"""
        if (gain == 1 or gain == 16):
            self.setGain(gain) # low/highGain
            ambient = self.readFull()
            IR = self.readIR()
        if (gain==0): # auto gain
            self.setGain(16) # first try highGain
            ambient = self.readFull()
            if (ambient < 65535):
                IR = self.readIR()
            if (ambient >= 65535 or IR >= 65535): # value(s) exeed(s) datarange
                self.setGain(1) # set lowGain
                ambient = self.readFull()
                IR = self.readIR()

        if (self.gain==1):
           ambient *= 16    # scale 1x to 16x
           IR *=16         # scale 1x to 16x
   
                       
        ratio= IR/float (ambient)

      

        if ((ratio >= 0) and (ratio <= 0.52)):
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

while True:
    tsl=TSL2561()
    #print tsl.readLux()
    
    print "LUX HIGH GAIN ", tsl.readLux(16)
    print "LUX LOW GAIN ", tsl.readLux(1)
    print "LUX AUTO GAIN ", tsl.readLux(0)
    print "\n\n"
    sleep (2)
