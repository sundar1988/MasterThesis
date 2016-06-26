import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24,GPIO.OUT)
pwmMotor=GPIO.PWM(24,500)
saveLux=[]

for pwm in range (0,101):# it runs from 0 to 100
    
    pwmMotor.start(pwm)
    time.sleep (0.2)
    import tsltry
    print pwm
    saveLux.append(tsltry.getLight())
    print tsltry.getLight()
    #print saveValue



#return "please select Lux between",saveLux[0], saveLux[100]
def selectLux(varLux):
    #varLux = raw_input("Enter lux value: ")
    #print "you entered ", varLux
    varLux= float(varLux)# change string to integer
    #print saveLux[varLux]
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
        if X1>99:
            X1=X0
        Y1 = saveLux[X1]
        
        print X0,Y0,X1,Y1
        
    else:
    
        X1 = saveLux.index(closeValue)
        Y1 = closeValue
        X0 = X1-1
        Y0 = saveLux[X0]
        print X0,Y0,X1,Y1
                   
    requiredPWM=((X1-X0)* ((varLux-Y0)/(Y1-Y0)))+(X0)

    return requiredPWM
#selectLux(75)

