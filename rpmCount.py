import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

input_A = 25
input_B = 23

GPIO.setup(input_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)


old_a = True
old_b = True
rpm=0

t0=time.time()

def get_encoder_turn():
    # return -1, 0, or +1
    global old_a, old_b
    result = 0
    new_a = GPIO.input(input_A)
    new_b = GPIO.input(input_B)
    if new_a != old_a or new_b != old_b :
        if old_a == 0 and new_a == 1 :
            result = (old_b * 2 - 1)
        elif old_b == 0 and new_b == 1 :
            result = -(old_a * 2 - 1)
    old_a, old_b = new_a, new_b
    time.sleep(0.001)
    return result

x = 0

while True:
    change = get_encoder_turn()
    if change != 0 :
        x = x + change
        t1=time.time()
        #try:
            #print(x)
            #print ("please wait calculating.....")
            #print((t1-t0))
#        except ZeroDivisionError:
 #           pass
                
        if t1-t0>=5:#each 5 sec
            y=x
            x=0
            rpm=y/3.416 #(y/41)*(60/5) --1 revolution is equal to 41 increment.
            #print (y)
            print "The motor RPM is:",rpm
            #print"\n"
            #print ("10sec")
            t0=t1
