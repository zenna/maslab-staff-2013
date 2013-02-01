import sys
sys.path.append("..")
import time

import sys    

def prog():    
    char = ""     
    while char != "/":    
        char = sys.stdin.read(1)    
        return char

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

def spool_stop():
	billy.spool.speed(0)

def spool_flow(speed):
	billy.spool.setSpeed(speed)

def spool_shift(speed):
	billy.spool.setSpeed(speed)
	time.sleep(1)
	billy.spool.setSpeed(0)

def latch():
	billy.latch.setAngle(0)

def unlatch():
	billy.latch.setAngle(110)

billy.motor_right.setSpeed(0)
billy.motor_left.setSpeed(0)
billy.roller.setSpeed(0)
# if __name__ == "__main__":
# 	go_fwd(1.0)
# 	go_bkwd(1.0)
# 	turn_left(1.0)
# 	turn_right(1.0)
# 	go_fwd(1.0)

# while True:
# 	char = prog()
# 	if char == "a":
# 		turn_left(1)
# 	elif char == "d"
# 		turn_right(1)
# 	elif char == "w"
# 		go_bkwd(1)
# 	elif char == "s"
# 		go_fwd(1)