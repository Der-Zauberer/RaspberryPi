import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pinMotorAForwards = 10
pinMotorABackwards = 9
pinMotorBForwards = 8
pinMotorBBackwards = 7

pinTrigger = 17
pinEcho = 18

Frequency = 50
DutyCycleA = 65
DutyCycleB = 65
Stop = 0

GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)

GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

HowNear = 25.0
ReverseTime = 0.5
TurnTime = 0.75

pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, Frequency)
pwmMotorABackwards = GPIO.PWM(pinMotorABackwards, Frequency)
pwmMotorBForwards = GPIO.PWM(pinMotorBForwards, Frequency)
pwmMotorBBackwards = GPIO.PWM(pinMotorBBackwards, Frequency)

pwmMotorAForwards.start(Stop)
pwmMotorABackwards.start(Stop)
pwmMotorBForwards.start(Stop)
pwmMotorBBackwards.start(Stop)

def StopMotors():
	pwmMotorAForwards.ChangeDutyCycle(Stop)
	pwmMotorABackwards.ChangeDutyCycle(Stop)
	pwmMotorBForwards.ChangeDutyCycle(Stop)
	pwmMotorBBackwards.ChangeDutyCycle(Stop)
	
def Forwards():
	pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
	pwmMotorABackwards.ChangeDutyCycle(Stop)
	pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
	pwmMotorBBackwards.ChangeDutyCycle(Stop)
	
def Backwards():
	pwmMotorAForwards.ChangeDutyCycle(Stop)
	pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
	pwmMotorBForwards.ChangeDutyCycle(Stop)
	pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)
	
def Left():
	pwmMotorAForwards.ChangeDutyCycle(Stop)
	pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
	pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
	pwmMotorBBackwards.ChangeDutyCycle(Stop)
	
def Right():
	pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
	pwmMotorABackwards.ChangeDutyCycle(Stop)
	pwmMotorBForwards.ChangeDutyCycle(Stop)
	pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)
	
def Measure():
	GPIO.output(pinTrigger, True)
	time.sleep(0.00001)
	GPIO.output(pinTrigger, False)
	StartTime = time.time()
	StopTime = StartTime
	
	while GPIO.input(pinEcho)==0:
		StartTime = time.time()
		StopTime = StartTime
	
	while GPIO.input(pinEcho)==1:
		StopTime = time.time()
		if StopTime-StartTime >= 0.04:
			print("Hold on there! You're too close for me to see.")
			StopTime = StartTime
			break
			
	ElapsedTime = StopTime - StartTime
	Distance = (ElapsedTime * 34326)/2
	return Distance
	
def IsNearObstacle(localHowNear):
	Distance = Measure()
	print("IsNearObstacle: "+str(Distance))
	if Distance < localHowNear:
		return True
	else:
		return False
		
def AvoidObstacle():
	print("Backwards")
	Backwards()
	time.sleep(ReverseTime)
	StopMotors()
	print("Right")
	Right()
	time.sleep(TurnTime)
	StopMotors()
	
try:
	
	GPIO.output(pinTrigger, False)
	time.sleep(0.1)
	
	while True:
		Forwards()
		time.sleep(0.1)
		if IsNearObstacle(HowNear):
			StopMotors()
			AvoidObstacle()
			
except KeyboardInterrupt:
	GPIO.cleanup()





