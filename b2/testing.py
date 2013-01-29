import sys
sys.path.append("..")
import time

import arduino

ard = arduino.Arduino()
sys.path.append("..")

motor_left = arduino.Motor(ard, 0, 42, 9, True)
motor_right = arduino.Motor(ard, 0, 38, 10, True)
roller = arduino.Motor(ard, 0, 48, 8, True)
ard.run() # Start the Arduino communication thread

def go_fwd(time_to_move):
	print "fwd"
	motor_left.setSpeed(50)
	motor_right.setSpeed(50)
	time.sleep(time_to_move)
	motor_left.setSpeed(0)
	motor_right.setSpeed(0)

def go_bkwd(time_to_move):
	print "bkwd"
	motor_left.setSpeed(-50)
	motor_right.setSpeed(-50)
	time.sleep(time_to_move)
	motor_left.setSpeed(0)
	motor_right.setSpeed(0)

def turn_left(time_to_move):
	print "left"
	motor_left.setSpeed(50)
	motor_right.setSpeed(-50)
	time.sleep(time_to_move)
	motor_left.setSpeed(0)
	motor_right.setSpeed(0)

def turn_right(time_to_move):
	print "right"
	motor_left.setSpeed(-50)
	motor_right.setSpeed(50)
	time.sleep(time_to_move)
	motor_left.setSpeed(0)
	motor_right.setSpeed(0)


# if __name__ == "__main__":
# 	go_fwd(1.0)
# 	go_bkwd(1.0)
# 	turn_left(1.0)
# 	turn_right(1.0)
# 	go_fwd(1.0)