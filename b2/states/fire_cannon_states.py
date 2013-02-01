from common import *
from state_machine import *

# Functions ending in body denote the main code that a state will execute
# Ready shoot state: moves the cannon into position ready for loading

# Global memory is global to a particular state machine, is used to communicate
# between states. e.g. global_mem["pid-gain"] = 5

# Local memory is local only to state and propositions

# act is the object of actuators, use this to move motors
# e.g. act["spool"].setSpeed(100)
# List of actuator is in main

# Env gives access to all environment stuff, switches, ir sensors
# camera etc.
# Because I havent found a better way first you need to get this state machines id
# sm_id = env["sync_value"]["state_machine_id"]
# then do ir_ball = env["pull_values"](sm_id, "ir_ball")
# Where you can replace ir_ball with any environment variable

# If you want to transition immediately to another state do
# return True, state_i_want_to_go_to_name
def ready_shoot_body(global_mem, local_mem, act, env, check_props):
	sm_id = env["sync_value"]["state_machine_id"]

	while True:		
		ir_ball = env["pull_values"](sm_id, "ir_ball")
		if ir_ball > 415:
			act["spool"].setSpeed(0)
			break
		act["spool"].setSpeed(-40)

	return False, None

def shoot_body(global_mem, local_mem, act, env, check_props):
	sm_id = env["sync_value"]["state_machine_id"]

	while True:
		high_button = env["pull_values"](sm_id, "high_button")
		if high_button == True:
			act["spool"].setSpeed(0)
			break
	act["spool"].setSpeed(40)

	return True, "ready_shoot"

# Propositions are sufficed prop for convetion
# and must return true or false
def ball_loaded_prop(global_mem, local_mem, act, env):
	sm_id = env["sync_value"]["state_machine_id"]
	ir_ball = env["pull_values"](sm_id, "ir_ball")
	if ir_ball > 500:
		return True
	else:
		return False

ready_shoot_propagators = [{'proposition':ball_loaded_prop, 'dst_state_id':"shoot"}]
ready_shoot_state = State(ready_shoot_body, no_propagators)

shoot_state = State(shoot_body, no_propagators)