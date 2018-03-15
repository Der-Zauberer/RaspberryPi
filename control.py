import RPi.GPIO as GPIO
from colorama import init, Fore, Style, Back
import time

init()

loop = True
hotkeymode = True
automaticmode = True

engine_left_forward = 10
engine_right_forward = 8
engine_left_backward = 9
engine_right_backward = 7

frequency = 50
duty_cycle = 75
stop = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(engine_left_forward ,GPIO.OUT)
GPIO.setup(engine_right_forward ,GPIO.OUT)
GPIO.setup(engine_left_backward ,GPIO.OUT)
GPIO.setup(engine_right_backward ,GPIO.OUT)

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
	
def engineOnRight():
	pwm_engine_left_forward.ChangeDutyCycle(duty_cycle)
	pwm_engine_right_forward.ChangeDutyCycle(stop)
	pwm_engine_left_backward.ChangeDutyCycle(stop)
	pwm_engine_right_backward.ChangeDutyCycle(duty_cycle)
	
def engineOnLeft():
	pwm_engine_left_forward.ChangeDutyCycle(stop)
	pwm_engine_right_forward.ChangeDutyCycle(duty_cycle)
	pwm_engine_left_backward.ChangeDutyCycle(duty_cycle)
	pwm_engine_right_backward.ChangeDutyCycle(stop)
	
def engineOnTimeForward():
	engine_time = input(Style.NORMAL + Fore.YELLOW + "Time: ")
	engineOnForward()
	time.sleep(int(engine_time))
	engineOff()
	
def engineOnTimeBackward():
	engine_time = input(Style.NORMAL + Fore.YELLOW + "Time: ")
	engineOnBackward()
	time.sleep(int(engine_time))
	engineOff()
	
def hotkeyhelp():
	print(Style.NORMAL + Fore.YELLOW + "help        - Open this interface")
	print("-w          - Go forward for 1 second slow")
	print("w           - Go forward for 1 second")
	print("ww  	       - Go forward for 2 seconds fast")
	print("wwww        - Go forward for 3 seconds very fast")
	print("a           - Go left for ~45°")
	print("aa          - Go left for ~90°")
	print("-s          - Go backward for 1 second slow")
	print("s           - Go backward for 1 second")
	print("ss          - Go backward for 1 second fast")
	print("d           - Go right for ~45°")
	print("dd          - Go right for ~90°")
	print("exit        - Leave the hotkeymode")
	
	
def help():
	print(Style.NORMAL + Fore.YELLOW + "help                   - Open this interface")
	print("engineOnForward        - Starts the engines forward")
	print("engineOnBackard        - Starts the engines backward")
	print("engineOnTimeForward    - Starts the engines forward with timelimit")
	print("engineOnTimeBackard    - Starts the engines backward with timelimit")
	print("engineOff              - Stopps engines")
	print("stop                   - Stopps engines")
	print("exit                   - Close programm  and cleanup GPIO")
	print("^C                     - Close programm and cleanup GPIO")
	
try:
	
	while loop == True:
		
		i = input(Style.BRIGHT + Fore.YELLOW + "RaspiControl $ " + Style.RESET_ALL)
		
		if(i == "engineOnForward"):
			engineOnForward(75)
			
		if(i == "engineOnBackward"):
			engineOnBackward(75)
			
		if(i == "engineOnTimeForward"):
			engineOnTimeForward()
			print(Style.NORMAL + Fore.YELLOW + "Successfully!")
			
		if(i == "engineOnTimeBackward"):
			engineOnTimeBackward()
			print(Style.NORMAL + Fore.YELLOW + "Successfully!")
			
		if(i == "engineOff"):
			engineOff()
			print(Style.NORMAL + Fore.YELLOW + "Successfully!")
			
		if(i == "stop"):
			engineOff()
			print(Style.NORMAL + Fore.YELLOW + "Successfully!")
			
		if(i == "hotkeymode"):
			while hotkeymode == True:
				
				ih = input(Style.BRIGHT + Fore.YELLOW + "RaspiControl - Hotkeymode $ " + Style.RESET_ALL)
				
				if(ih == "exit"):
					hotkeymode = False
					
				if(ih == "help"):
					hotkeyhelp()
					
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
					engineOnLeft()
					time.sleep(0.56)
					engineOff()
					
				if(ih == "aa"):
					engineOnLeft()
					time.sleep(1.3)
					engineOff()
					
				if(ih == "d"):
					engineOnRight()
					time.sleep(0.56)
					engineOff()
					
				if(ih == "dd"):
					engineOnRight()
					time.sleep(1.3)
					engineOff()
					
		if(i == "automaticmode"):
			while automaticmode == True:
				
				ih = input(Style.BRIGHT + Fore.YELLOW + "RaspiControl - Automaticmode $ " + Style.RESET_ALL)
				
				if(ih == "exit"):
					automaticmode = False
			
		if(i == "help"):
			help()
			
		if(i == "exit"):
			GPIO.cleanup()
			loop = False
			

except KeyboardInterrupt:
	GPIO.cleanup()
	print("")
