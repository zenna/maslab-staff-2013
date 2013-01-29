import sys
sys.path.append("..")
import time

from billy import *

import arduino

ard = arduino.Arduino()
sys.path.append("..")

billy = Billy()
billy.init_arduino()

def go_fwd(time_to_move):
	print "fwd"
	billy.motor_left.setSpeed(50)
	billy.motor_right.setSpeed(50)
	time.sleep(time_to_move)
	billy.motor_left.setSpeed(0)
	billy.motor_right.setSpeed(0)

def go_bkwd(time_to_move):
	print "bkwd"
	billy.motor_left.setSpeed(-50)
	billy.motor_right.setSpeed(-50)
	time.sleep(time_to_move)
	billy.motor_left.setSpeed(0)
	billy.motor_right.setSpeed(0)

def turn_left(time_to_move):
	print "left"
	billy.motor_left.setSpeed(50)
	billy.motor_right.setSpeed(-50)
	time.sleep(time_to_move)
	billy.motor_left.setSpeed(0)
	billy.motor_right.setSpeed(0)

def turn_right(time_to_move):
	print "right"
	billy.motor_left.setSpeed(-50)
	billy.motor_right.setSpeed(50)
	time.sleep(time_to_move)
	billy.motor_left.setSpeed(0)
	billy.motor_right.setSpeed(0)


# if __name__ == "__main__":
# 	go_fwd(1.0)
# 	go_bkwd(1.0)
# 	turn_left(1.0)
# 	turn_right(1.0)
# 	go_fwd(1.0)