## Proposition: activated when close to walls
def close_to_wall_prop(global_memory, local_memory, rcvd_msg, env):
	WALL_THRESHOLD = 400
	if env.ir < WALL_THRESHOLD:
		return True
	else:
		return False
## State: activated when close to walls
def avoid_wall_state(global_memory, local_memory, act):
	print "State: avoid_wall"
	act["motor_left"].setSpeed(-100)
	act["motor_right"].setSpeed(-100)

	#turn for random time from 0-3 secs
	time.sleep(rand.random()*3)

go_to_avoid_wall = {'proposition':close_to_wall, 'dst_state_id':"avoid_wall"}