import cv2
import cv2.cv as cv
import time
import numpy as np
import random
import time

import billy
from states import *
from thalamus import *

# Reduce image size
def bgr_to_hsv(img):
	# Convert from BGR to HSV
	hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
	cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
	return hsv

def threshold_green_balls(img):
	# Threshold the img in hsv space for green
	img_thresh = cv.CreateImage(cv.GetSize(img), 8, 1)
	cv2.cv.InRangeS(img, cv.Scalar(180*145/360, 100, 84), cv.Scalar(180*165/360, 220, 255), img_thresh)
	return img_thresh

def go_fwd(act,img):
	print "going fwd"
	# act.motor_left.setSpeed(100)
	# act.motor_right.setSpeed(100)

def go_bkwd(act,img):
	print "going bckwd"
	# act.motor_left.setSpeed(100)
	# act.motor_right.setSpeed(-100)

def time_is_even(rcvd_msg, img):
	now = time.time()
	if int(now) % 20 == 0:
		return True
	else:
		return False

def do_nothing():
	pass

if __name__ == "__main__":
	b4 = billy.Billy()
	b4.init_arduino() #Get serial port for attiny
	b4.init_camera(0) # Camera id is typically 1

	# A state machine could have a number of slots it can write to
	# and these slots are mapped by a separate process to an actuator
	actuators = {"motor_left": b4.motor_left, "motor_right": b4.motor_right}
	wheel_controllers = StateMachine(actuators)

	propagator = [{"proposition": time_is_even, "dst_state_id": "go_bkwd"}]
	go_fwd_state = State(do_nothing, go_fwd, propagator)
	go_bkwd_state = State(do_nothing, go_bkwd, [])
	
	wheel_controllers.add_state(go_fwd_state, "go_fwd")
	wheel_controllers.add_state(go_bkwd_state, "go_bkwd")
	wheel_controllers.set_current_state("go_fwd")

	thalamus = ThalamicNetwork()

	thalamus.add_modulator(b4.get_ir, "get_ir")
	thalamus.add_modulator(threshold_green_balls, "threshold_green_balls")
	thalamus.add_modulator(b4.get_frame, "get_frame")
	thalamus.add_modulator(bgr_to_hsv, "bgr_to_hsv")
	thalamus.add_state_machine(wheel_controllers, "wheel_controllers")

	thalamus.link_nodes("get_frame", "bgr_to_hsv", "img")
	thalamus.link_nodes("bgr_to_hsv", "threshold_green_balls", "img")
	thalamus.link_nodes("threshold_green_balls", "wheel_controllers", "img")

	thalamus.run_serial()