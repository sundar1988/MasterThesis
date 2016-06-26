from Tkinter import *
import RPi.GPIO as GPIO
import time
import cgi

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
pwmMotor1 = GPIO.PWM(4, 500)
pwmMotor1.start(0)
pwmMotor2 = GPIO.PWM(18, 500)
pwmMotor2.start(0)
pwmStreetLamp = GPIO.PWM(17, 100)
pwmStreetLamp.start(0)

class App:
        
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        Label(frame, text='Cable Car').grid(row=0, column=0)
        Label(frame, text='Wind Mills').grid(row=1, column=0)
        Label(frame, text='Street Lamp').grid(row=4, column=0)
        scaleMotor1 = Scale(frame, from_=0, to=100, 
              orient=HORIZONTAL, command=self.updateMotor1)
        scaleMotor1.grid(row=0, column=1)
        scaleMotor2 = Scale(frame, from_=0, to=100, 
              orient=HORIZONTAL, command=self.updateMotor2)
        scaleMotor2.grid(row=1, column=1)
        scaleStreetLamp = Scale(frame, from_=0, to=100, 
              orient=HORIZONTAL, command=self.updateStreetLamp)
        scaleStreetLamp.grid(row=4, column=1)

    def updateMotor1(self, duty):
        pwmMotor1.ChangeDutyCycle(float(duty))
    def updateMotor2(self, duty):
        pwmMotor2.ChangeDutyCycle(float(duty))
    def updateStreetLamp(self, duty):
        pwmStreetLamp.ChangeDutyCycle(float(duty))

root = Tk()
root.wm_title('PWM Speed+Brightness')
app = App(root)
root.geometry("400x200+0+0")
root.mainloop()
