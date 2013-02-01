from common import *
from state_machine import *

def ready_shoot_body(global_memory, local_memory, act, env, check_props):
	act["spool"].setSpeed(-40)
	sm_id = env["sync_value"]["state_machine_id"]

	while True:		
		ir_ball = env["pull_values"](sm_id, "ir_ball")
		if ir_ball > 415:
			act["spool"].setSpeed(0)
			break

	return True, "shoot"

def shoot_body(global_memory, local_memory, act, env, check_props):
	act["spool"].setSpeed(40)
	sm_id = env["sync_value"]["state_machine_id"]

	while True:
		high_button = env["pull_values"](sm_id, "high_button")
		if high_button == True:
			act["spool"].setSpeed(0)
			break

	return True, "ready_shoot"

def ball_loaded_prop(global_memory, local_memory, act, env):
	sm_id = env["sync_value"]["state_machine_id"]
	ir_ball = env["pull_values"](sm_id, "ir_ball")
	if ir_ball > 500:
		return True
	else:
		return False

ready_shoot_propagators = [{'proposition':ball_loaded_prop, 'dst_state_id':"shoot"}]
ready_shoot_state = State(ready_shoot_body, no_propagators)

shoot_state = State(shoot_body, no_propagators)