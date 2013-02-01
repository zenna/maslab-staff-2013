## Proposition: activated when close to walls

def close_to_wall_prop(global_memory, local_memory, rcvd_msg, env):
	WALL_THRESHOLD = 400
	# change this to an or of the left and right sensors
	sm_id = env["sync_value"]["state_machine_id"]
	ir_tuple= env["pull_value"](sm_id, "get_ir")
	if ir_tuple[0] < WALL_THRESHOLD or ir_tuple[2] < WALL_THRESHOLD:
		return True
	else:
		return False
## State: activated when close to walls
def avoid_wall_state(global_memory, local_memory, act):
	sm_id = env["sync_value"]["state_machine_id"]
	print "State: avoid_wall"
	act["motor_left"].setSpeed(-100)
	act["motor_right"].setSpeed(-100)

	#turn for random time from 0-3 secs
	time.sleep(rand.random()*3)

	#return ???

go_to_avoid_wall = {'proposition':close_to_wall, 'dst_state_id':"avoid_wall"}
