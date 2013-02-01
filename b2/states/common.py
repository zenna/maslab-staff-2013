# These are common functions and propagators used by states
import numpy as np
import time

from states import *
## Common Propogators
def time_over_prop(global_mem, local_memory, rcvd_msg, env):
	if time.time() - global_mem['start_time'] > 178:
		return True
	else:
		return False
go_to_ready = {'proposition':time_over_prop, 'dst_state_id':"ready"}
no_propagators = []

def am_init(global_memory, local_memory, rcvd_msg, env):
	if "initialised" in local_memory and local_memory['initialised'] == True:
		return True
	else:
		return False

## COMMON functions
def go_fwd(act, speed):
	act["motor_left"].setSpeed(speed)
	act["motor_right"].setSpeed(speed)

def go_bkwd(act, speed):
	act["motor_left"].setSpeed(-speed)
	act["motor_right"].setSpeed(-speed)

def turn_left(act, speed):
	act["motor_left"].setSpeed(speed)
	act["motor_right"].setSpeed(-speed)

def turn_right(act, speed):
	act["motor_left"].setSpeed(-speed)
	act["motor_right"].setSpeed(speed)

def stop_wheels(act):
	act["motor_left"].setSpeed(0)
	act["motor_right"].setSpeed(0)
	act["roller"].setSpeed(0)

def roller_on(act):
	act["roller"].setSpeed(126)

def roller_off(act):
	act["roller"].setSpeed(0)

def turn_to_orient(act, env, orient, speed):
	print "orienting to"
	sm_id = env["sync_value"]["state_machine_id"]
	current_orientation = env["pull_value"](sm_id,"get_imu")[3]
	turn_left(act, speed)
	while True:
		curr = abs(env["pull_value"](sm_id,"get_imu")[0] - orient)
		print "current - to", curr, orient
		if curr < 10:
			break

def clamp(speed, top_speed):
    if speed < -top_speed:
        speed = -top_speed
    elif speed > top_speed:
        speed = top_speed

    return speed

def move_differential(adjustment,global_mem,act):
    global_mem["motor_left_speed"] = global_mem["motor_left_speed"] + adjustment
    global_mem["motor_right_speed"] = global_mem["motor_right_speed"] - adjustment    

    # global_mem["motor_left_speed"] = clamp(global_mem["motor_left_speed"],30)
    # global_mem["motor_right_speed"] = clamp(global_mem["motor_right_speed"],30)

    print "SENDING SPEED", global_mem["motor_left_speed"], global_mem["motor_right_speed"]
    act["motor_left"].setSpeed(global_mem["motor_left_speed"])
    act["motor_right"].setSpeed(global_mem["motor_right_speed"])