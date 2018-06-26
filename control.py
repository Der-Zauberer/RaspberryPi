import RPi.GPIO as GPIO
from colorama import init, Fore, Style, Back
import time

init()

loop = True
lineloop = True
hotkeymode = True
testmode = True
automaticmode = True

engine_left_forward = 10
engine_right_forward = 8
engine_left_backward = 9
engine_right_backward = 7

line_detector = 4
frequency = 50
stop = 0

HowNear = 30.0
ReverseTime = 0.6
TurnTime = 0.75

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(engine_left_forward ,GPIO.OUT)
GPIO.setup(engine_right_forward ,GPIO.OUT)
GPIO.setup(engine_left_backward ,GPIO.OUT)
GPIO.setup(engine_right_backward ,GPIO.OUT)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.IN)

pwm_engine_left_forward = GPIO.PWM(engine_left_forward, frequency)
pwm_engine_right_forward = GPIO.PWM(engine_right_forward, frequency)
pwm_engine_left_backward = GPIO.PWM(engine_left_backward, frequency)
pwm_engine_right_backward = GPIO.PWM(engine_right_backward, frequency)

pwm_engine_left_forward.start(stop)
pwm_engine_right_forward.start(stop)
pwm_engine_left_backward.start(stop)
pwm_engine_right_backward.start(stop)
	
def engineOff():
	pwm_engine_left_forward.ChangeDutyCycle(stop)
	pwm_engine_right_forward.ChangeDutyCycle(stop)
	pwm_engine_left_backward.ChangeDutyCycle(stop)
	pwm_engine_right_backward.ChangeDutyCycle(stop)
	
def engineOnForward(speed):
	pwm_engine_left_forward.ChangeDutyCycle(speed)
	pwm_engine_right_forward.ChangeDutyCycle(speed)
	pwm_engine_left_backward.ChangeDutyCycle(stop)
	pwm_engine_right_backward.ChangeDutyCycle(stop)
	
def engineOnBackward(speed):
	pwm_engine_left_forward.ChangeDutyCycle(stop)
	pwm_engine_right_forward.ChangeDutyCycle(stop)
	pwm_engine_left_backward.ChangeDutyCycle(speed)
	pwm_engine_right_backward.ChangeDutyCycle(speed)
	
def engineOnRight(speed):
	pwm_engine_left_forward.ChangeDutyCycle(speed)
	pwm_engine_right_forward.ChangeDutyCycle(stop)
	pwm_engine_left_backward.ChangeDutyCycle(stop)
	pwm_engine_right_backward.ChangeDutyCycle(speed)
	
def engineOnLeft(speed):
	pwm_engine_left_forward.ChangeDutyCycle(stop)
	pwm_engine_right_forward.ChangeDutyCycle(speed)
	pwm_engine_left_backward.ChangeDutyCycle(speed)
	pwm_engine_right_backward.ChangeDutyCycle(stop)
	
def engineOnTimeForward(speed):
	engine_time = input(Style.NORMAL + Fore.YELLOW + "Time: ")
	engineOnForward(speed)
	time.sleep(int(engine_time))
	engineOff()
	
def engineOnTimeBackward(speed):
	engine_time = input(Style.NORMAL + Fore.YELLOW + "Time: ")
	engineOnBackward(speed)
	time.sleep(int(engine_time))
	engineOff()

def isBlack():
        if GPIO.input(line_detector)==0:
                return True
        else:
                return False
	
def Measure():
	GPIO.output(17, True)
	time.sleep(0.00001)
	GPIO.output(17, False)
	StartTime = time.time()
	StopTime = StartTime
	
	while GPIO.input(18)==0:
		StartTime = time.time()
		StopTime = StartTime
	
	while GPIO.input(18)==1:
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
	engineOnBackward(60)
	time.sleep(ReverseTime)
	engineOff()
	print("Right")
	engineOnRight(50)
	time.sleep(TurnTime)
	engineOff()
	
def hotkeymodehelp():
	print(Style.NORMAL + Fore.YELLOW + "help        - Open this interface")
	print("-w          - Go forward for 1 second slow")
	print("w           - Go forward for 1 second")
	print("ww  	   - Go forward for 2 seconds fast")
	print("wwww        - Go forward for 3 seconds very fast")
	print("a           - Go left for ~45°")
	print("aa          - Go left for ~90°")
	print("-s          - Go backward for 1 second slow")
	print("s           - Go backward for 1 second")
	print("ss          - Go backward for 1 second fast")
	print("d           - Go right for ~45°")
	print("dd          - Go right for ~90°")
	print("exit        - Leave the hotkeymode")
	
def testmodehelp():
	print(Style.NORMAL + Fore.YELLOW + "help                   - Open this interface")
	print("engineOnForward        - Starts the engines forward")
	print("engineOnBackard        - Starts the engines backward")
	print("engineOnTimeForward    - Starts the engines forward with timelimit")
	print("engineOnTimeBackard    - Starts the engines backward with timelimit")
	print("engineOff              - Stopps engines")
	print("stop                   - Stopps engines")
	print("exit                   - Leave the testmode")
	
def testmodehelp():
	print(Style.NORMAL + Fore.YELLOW + "help                   - Open this interface")
	print("engineOff              - Stopps engines")
	print("stop                   - Stopps engines")
	print("exit                   - Leave the automaticmode")
	
def help():
	print(Style.NORMAL + Fore.YELLOW + "help                   - Open this interface")
	print("stop                   - Stopps engines")
	print("testmode               - Go in Testmode")
	print("hotkeymode             - Go in Hotkeymode")
	print("automaticmode          - Go in Automaticmode")
	print("exit                   - Close programm  and cleanup GPIO")
	print("^C                     - Close programm and cleanup GPIO")
	
try:
	
	while loop == True:
		
		i = input(Style.BRIGHT + Fore.YELLOW + "RaspiControl $ " + Style.RESET_ALL)
			
		if(i == "stop"):
			engineOff()
			print(Style.NORMAL + Fore.YELLOW + "Successfully!")
			
		if(i == "testmode"):
			while testmode == True:
			
				ite = input(Style.BRIGHT + Fore.YELLOW + "RaspiControl - Testmode $ " + Style.RESET_ALL)
			
				if(ite == "exit"):
					testmode = False
				
				if(ite == "help"):
					testmodehelp()
			
				if(ite == "engineOnForward"):
					engineOnForward(75)
			
				if(ite == "engineOnBackward"):
					engineOnBackward(75)
			
				if(ite == "engineOnTimeForward"):
					engineOnTimeForward(75)
					print(Style.NORMAL + Fore.YELLOW + "Successfully!")
			
				if(ite == "engineOnTimeBackward"):
					engineOnTimeBackward(75)
					print(Style.NORMAL + Fore.YELLOW + "Successfully!")
			
				if(ite == "engineOff"):
					engineOff()
					print(Style.NORMAL + Fore.YELLOW + "Successfully!")
			
				if(ite == "stop"):
					engineOff()
					print(Style.NORMAL + Fore.YELLOW + "Successfully!")
			
		if(i == "hotkeymode"):
			while hotkeymode == True:
				
				ih = input(Style.BRIGHT + Fore.YELLOW + "RaspiControl - Hotkeymode $ " + Style.RESET_ALL)
				
				if(ih == "exit"):
					hotkeymode = False
					
				if(ih == "help"):
					hotkeymodehelp()
					
				if(ih == "-w"):
					engineOnForward(40)
					time.sleep(1)
					engineOff()
					
				if(ih == "w"):
					engineOnForward(75)
					time.sleep(1)
					engineOff()
					
				if(ih == "ww"):
					engineOnForward(85)
					time.sleep(2)
					engineOff()
					
				if(ih == "www"):
					engineOnForward(95)
					time.sleep(3)
					engineOff()
					
				if(ih == "-s"):
					engineOnBackward(40)
					time.sleep(1)
					engineOff()	
				
				if(ih == "s"):
					engineOnBackward(50)
					time.sleep(1)
					engineOff()
					
				if(ih == "ss"):
					engineOnBackward(60)
					time.sleep(2)
					engineOff()
					
				if(ih == "a"):
					engineOnLeft(75)
					time.sleep(0.56)
					engineOff()
					
				if(ih == "aa"):
					engineOnLeft(75)
					time.sleep(1.3)
					engineOff()
					
				if(ih == "d"):
					engineOnRight(75)
					time.sleep(0.56)
					engineOff()
					
				if(ih == "dd"):
					engineOnRight(75)
					time.sleep(1.3)
					engineOff()
					
		if(i == "automaticmode"):
			while automaticmode == True:
				
				ih = input(Style.BRIGHT + Fore.YELLOW + "RaspiControl - Automaticmode $ " + Style.RESET_ALL)
				
				if(ih == "obstacle"):
					GPIO.output(17, False)
					time.sleep(0.1)
					while True:
						engineOnForward(60)
						time.sleep(0.1)
						if IsNearObstacle(HowNear):
							engineOff()
							AvoidObstacle()
							
				if(ih == "line"):
					engineOnLeft(50)
					while(lineloop == True):
						if IsNearObstacle(20):
							engineOff()
							lineloop = False
						if isBlack():
							engineOff()
							lineloop = False
				
				if(ih == "exit"):
					automaticmode = False
					
				if(ih == "help"):
					automaticmodehelp()
		
		if(i == "help"):
			help()
			
		if(i == "exit"):
			GPIO.cleanup()
			loop = False
			
		hotkeymode = True
		testmode = True
		automaticmode = True
		
except KeyboardInterrupt:
	GPIO.cleanup()
	print("")
