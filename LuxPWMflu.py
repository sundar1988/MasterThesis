#!/usr/bin/python
## Date:        11.06.2014
## Author:      Sundar Shrestha

##------------Overview-------------------------------------------------
# save relative lux values as the light get brighter from 0...4096 pulse value
# this saves the lux value of front down lamp
# respective lux sensor is sensor having I2c address 0x39
# function selectLux determines the pulse value respected to user inputed lux value
##----------------------------------------------------------------------
import time
import LuxSensor39
from drivePWM import select

## import excel workbook----------
import xlwt     
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

saveLux=[]
time.sleep(2)
LuxSensor39.enable()
    
for i in range (0,4097,16):# 16 is step size choosen which lead to change the requiredPWM value
    
    select(2,i)
    time.sleep(0.1)
    saveLux.append(LuxSensor39.getLight())
LuxSensor39.disable()

## saving in .xls file----------
j=0
for n in saveLux:
    sheet1.write(j, 0, j)
     
    sheet1.write(j, 1, n)
    j = j+1
book.save("trial.xls")

def selectLux(varLux):
    varLux= float(varLux)# change string to integer
    closeValue = min(saveLux, key=lambda x:abs(x-varLux))# find the closest number in saveLux
                                              # to the given lux value 
    
    if varLux > closeValue:        
        X0 = saveLux.index(closeValue)
        for i in range (0,8):
            if saveLux[X0]== saveLux[X0+1]:
                X0=X0+1
            else:
                X0=X0
        
        Y0 = closeValue
        X1 = X0+1
        if X1>256: # the last step is 256 for each increment 16 (4096/16 =256)
            X1=X0
        Y1 = saveLux[X1]
       
        
    else:
    
        X1 = saveLux.index(closeValue)
        Y1 = closeValue
        X0 = X1-1
        Y0 = saveLux[X0]
             
    requiredPWM=((X1-X0)* ((varLux-Y0)/(Y1-Y0)))+(X0)
    requiredPWMactual=int(requiredPWM*16) # 16 is step size choosen
                                          # int is due to drivePWM

    return requiredPWMactual
