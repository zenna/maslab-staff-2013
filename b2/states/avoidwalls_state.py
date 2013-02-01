from common import *
from state_machine import *

## Proposition: activated when close to walls

def close_to_wall_prop(global_mem, local_mem, act, env):
	print "checking close to wall"
	WALL_THRESHOLD = 400
	# change this to an or of the left and right sensors
	sm_id = env["sync_value"]["state_machine_id"]
	ir_tuple= env["pull_value"](sm_id, "get_ir")
	if ir_tuple[0] > WALL_THRESHOLD or ir_tuple[2] > WALL_THRESHOLD:
		return True	
	else:
		return False

## State: activated when close to walls
def avoid_wall_body(global_mem, local_mem, act, env, check_props):
	print "avoid walls"
	sm_id = env["sync_value"]["state_machine_id"]
	print "State: avoid_wall"
	act["motor_left"].setSpeed(-70)
	act["motor_right"].setSpeed(-70)

	#turn for random time from 0-3 secs
	time.sleep(rand.random()*3)
	return True, global_mem["previous_state"]

avoid_wall_state = State(avoid_wall_body,[])