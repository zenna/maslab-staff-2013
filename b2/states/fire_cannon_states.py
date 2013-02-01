from common import *
from state_machine import *

def ready_shoot_body(global_memory, local_memory, act, env, check_props):
	act["spool"].setSpeed(-40)
	sm_id = env["sync_value"]["state_machine_id"]

	while True:
		low_button = env["pull_values"](sm_id, "low_button")
		if low_button == True:
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

# def ball_loaded_prop(global_memory, local_memory, act, env):
# 	if env["pull_values"]()

ready_shoot_state = State(ready_shoot_body, no_propagators)
shoot_state = State(shoot_body, no_propagators)