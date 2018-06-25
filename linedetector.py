import RPi.GPIO as GPIO
import time

loop = true

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pinLineFollower = 4

GPIO.setup(pinLineFollower, GPIO.IN)

try:
    while loop == True:
        if GPIO.input(pinLineFollower)==0:
            print("Black")
        else:
            print("White")
        time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.clearup()
