from tkinter import *
from tkinter import ttk
import sys
import time
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

#GPIO import
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

pwmStreetLamp = GPIO.PWM(18,5000)
pwmStreetLamp.start(0)

pwmRightLamp = GPIO.PWM(23,5000)
pwmRightLamp.start(0)

pwmLeftLamp = GPIO.PWM(24,5000)
pwmLeftLamp.start(0)

pwmFrontUpLamp = GPIO.PWM(25,5000)
pwmFrontUpLamp.start(0)

#pwmFrontMiddleLamp = GPIO.PWM(25,5000)
#pwmFrontMiddleLamp.start(0)

#pwmFrontDownLamp = GPIO.PWM(25,5000)
#pwmFrontDownLamp.start(0)



class Lamp:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        Label(frame, text='Street Lamp').grid(row=4, column=0)
        Label(frame, text='Right Lamp').grid(row=5, column=0)
        Label(frame, text='Left Lamp').grid(row=6, column=0)
        Label(frame, text='Front Up Lamp').grid(row=7, column=0)
        Label(frame, text='Front Middle Lamp').grid(row=8, column=0)
        Label(frame, text='Front Down Lamp').grid(row=9, column=0)
        #scale
        scaleStreetLamp = ttk.Scale(root, orient=HORIZONTAL, length=100, from_ =1.0, to =100.0, command=self.updateStreetLamp)
        scaleStreetLamp.grid (column=2, row=4, sticky=E)
        
        scaleRightLamp = ttk.Scale(root, orient=HORIZONTAL, length=100, from_ =1.0, to =100.0, command=self.updateRightLamp)
        scaleRightLamp.grid (column=2, row=5, sticky=E)
        
        
        scaleLeftLamp = ttk.Scale(root, orient=HORIZONTAL, length=100, from_ =1.0, to =100.0, command=self.updateLeftLamp)
        scaleLeftLamp.grid (column=2, row=6, sticky=E)
        
        scaleFrontUpLamp = ttk.Scale(root, orient=HORIZONTAL, length=100, from_ =1.0, to =100.0, command=self.updateFrontUpLamp)
        scaleFrontUpLamp.grid (column=2, row=7, sticky=E)
        
        scaleFrontMiddleLamp = ttk.Scale(root, orient=HORIZONTAL, length=100, from_ =1.0, to =100.0, command=self.updateFrontMiddleLamp)
        scaleFrontMiddleLamp.grid (column=2, row=8, sticky=E)
        
        scaleDownLamp = ttk.Scale(root, orient=HORIZONTAL, length=100, from_ =1.0, to =100.0, command=self.updateFrontDownLamp)
        scaleDownLamp.grid (column=2, row=9, sticky=E)

    def updateStreetLamp(self, duty):
        pwmStreetLamp.ChangeDutyCycle(float(duty))
    def updateRightLamp(self, duty):
        pwmRightLamp.ChangeDutyCycle(float(duty))
        
    def updateLeftLamp(self, duty):
        pwmLefttLamp.ChangeDutyCycle(float(duty))
           
    def updateFrontUpLamp(self, duty):
        pwmFrontUpLamp.ChangeDutyCycle(float(duty))
        
    def updateFrontMiddleLamp(self, duty):
        pwmFrontMiddleLamp.ChangeDutyCycle(float(duty))
        
    def updateFrontDownLamp(self, duty):
        pwmFrontDownLamp.ChangeDutyCycle(float(duty)) 



def mAbout ():
    messagebox.showinfo (title="About", message="This is my about box")
    return
def mQuit ():
    mExit= messagebox.askyesno(title="Quit", message="Are you sure ?")
    if mExit > 0:       
        root.destroy()
        return
def mOpen ():

    mOpen= filedialog.askopenfile()
    return

def mSaveas ():
    #mSaveas= filedialog.asksavefile
    return

    


lbl1=ttk.Label(c, text="Select Brightness:")

lbl1.grid(column=1, row=7, sticky=(E,S))


##################Event binding######################
# Set event bindings for when the selection in the listbox changes,
# when the user double clicks the list, and when they hit the Return key






#sizegrip
ttk.Sizegrip(root).grid(column=999, row=999, sticky=E)






#################Menu construction############################

menubar = Menu(root)
#file menu
filemenu=Menu(menubar,tearoff=0)

filemenu.add_command(label="New")
filemenu.add_command(label="Open", command=mOpen)
filemenu.add_command(label="Save As...", command=mSaveas)
filemenu.add_command(label="Close", command = mQuit)
menubar.add_cascade(label="File", menu=filemenu)

#help menu
helpmenu=Menu(menubar,tearoff=0)
helpmenu.add_command(label="About", command=mAbout)
helpmenu.add_command(label="GUI docs")
helpmenu.add_command(label="More help")
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

###################combobox##########################
country = ttk.Combobox(root, textvariable=countryvar)
country.grid(column=2, row=1, sticky=(E))#--sticking feet entry
#country.bind('<<manmm>>', meter)
country['values'] = ('combo', 'box', 'example')


root = Tk()
root.title("Controller Module")

# Set the starting state of the interface, including selecting the
# default gift to send, and clearing the messages. Select the first
# country in the list; because the <<ListboxSelect>> event is only
# generated when the user makes a change, we explicitly call showPopulation.
gift.set('flowers')
sentmsg.set('')
statusmsg.set('')
lbox.selection_set(0)
showPopulation()
lamp = Lamp(root)
root.mainloop()


