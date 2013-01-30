import numpy as np
import time
import cv2
import cv2.cv as cv

from states import *
import random

#without explicit initialiation, how to ensure thigns only get called once

# Make all states go to shutdown after 180 seconds
# Make ready state take environment variable red/green
#

## Common Propogators
def time_over(global_mem, local_memory, rcvd_msg, env):
	if time.time() - global_mem['start_time'] > 179:
		return True
	else:
		return False

go_to_ready = {'proposition':time_over, 'dst_state_id':"ready_state"}

## Don't get stuck state!
def close_to_wall(global_memory, local_memory, rcvd_msg, env):
	WALL_THRESHOLD = 400
	if env.ir < WALL_THRESHOLD:
		return True
	else:
		return False

def avoid_wall(global_memory, local_memory, act):
	print "State: avoid_wall"
	act["motor_left"].setSpeed(-100)
	act["motor_right"].setSpeed(-100)

	#turn for random time from 0-3 secs
	time.sleep(rand.random()*3)

go_to_avoid_wall = {'proposition':close_to_wall, 'dst_state_id':"avoid_wall"}

## Commonly used state functions
def stop_wheels(act):
	act["motor_left"].setSpeed(0)
	act["motor_right"].setSpeed(0)
	act["roller"].setSpeed(0)

## Ready State : initialisation and ready to go
def ready_state(global_mem, local_mem, act, env):
	# This state initialises memory and gets ready for the button press
	print "In ready state"
	stop_wheels(act)
	if "initialised" not in local_mem:
		global_mem['start_time'] = time.time()
		#PID controller, tuning params:
		# cv.NamedWindow("camera", 1)
		global_mem["proportional_gain"] = .2
		global_mem["integral_gain"] = .01
		global_mem["derivative_gain"] = 2
		window_size = 1000	
		global_mem["past_errors"] = {'errors':np.zeros([window_size]),'timestamps':np.zeros([window_size])}
		local_mem["initialised"] = True

		# Centroid Init
		global_mem["cam_width"] = cam_width = 640
		global_mem["cam_height"] = cam_height = 480

		# FIXME: Pobably these indices should be local memory
		global_mem["indices_x"] = np.tile(range(cam_width),[cam_height,1])
		indices_y = np.tile(range(cam_width),[cam_width,1]).transpose()
		global_mem["indices_y"] = indices_y[0:cam_height,0:cam_width]

	cv.ShowImage("camera", env["img"])
	x,y = find_centroid(env["img"], global_mem["cam_width"], global_mem["cam_height"], global_mem['indices_x'], global_mem['indices_x'])
	global_mem['y'] = y
	cv.WaitKey(10)

def am_init(global_memory, local_memory, rcvd_msg, env):
	if "initialised" in local_memory and local_memory['initialised'] == True:
		return True
	else:
		return False

def reset_switch_down(global_mem, local_mem, rcvd_msg, env):
	if global_mem['y'] > 500:
		return True
	else:
		return False
	return env.reset_switch_down

def ready_prop(global_memory, local_memory, rcvd_msg, env):
	return am_init(global_memory, local_memory, rcvd_msg, env) and reset_switch_down(global_memory, local_memory, rcvd_msg, env)

# ready -> explore
propagators = [{'proposition':ready_prop, 'dst_state_id':"explore"}]
ready_state = State(ready_state, propagators)

## Explore State : look for balls
# Problem what if I want to use an environment state at two different times
# HACK - just access it directly
# Sol 1 - Go tp pull model, maybe even in addition to current model
# Sol 2 - Go to parallel code, env.ir.ir_centre is a voltative value
# Sol 3 - 
def explore(global_memory, local_memory, act, env):
	ir = env.ir.ir_centre
	rotate(global_memory, local_memory, act)

explore_state = State(explore, [])
explore_propagators = [go_to_ready, go_to_avoid_wall]

## Don't get stuck state!
def rotate(global_memory, local_memory, act, env):
	print "State: rotate"
	act.motor_left.setSpeed(-100)
	act.motor_right.setSpeed(-100)
	time.sleep()

## Seek a ball in view
from pid import *

def seek_ball(global_memory, local_memory, act, env):
	#Calculate motor out with PID controller
	error_current = position_error(x,y)
	np.roll(global_mem["past_errors"]['errors'],-1)
	np.roll(global_mem["past_errors"]['timestamps'],-1)
	global_mem["past_errors"]['errors'][-1] = error_current
	global_mem["past_errors"]['timestamps'][-1] = time_current
	derivative_out = find_deriviative(past_errors)
	integral_out = integrate_errors(past_errors)
	controller_out = proportional_gain * error_current + integral_gain * integral_out + derivative_gain * derivative_out
	move_differential(controller_out, act)