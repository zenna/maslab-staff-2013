from common import *
from state_machine import *

#State :  explore, look for balls
def explore_body(global_memory, local_memory, act, env):
	# Do one full revolution using IMU
	print "exploring"
	sm_id = env["sync_value"]["state_machine_id"]
	current_orientation = env["pull_value"](sm_id,"get_imu")[0]
	one_eight_deg = (current_orientation + 180) % 360

	turn_to_orient(act, env, one_eight_deg, 20)

	import ipdb
	ipdb.set_trace()

	turn_left(act)
	orients = []
	irs = []
	while True:
		env["pull_value"](sm_id,"get_imu")[0]
		orients.append(env["pull_value"](sm_id,"get_imu")[0])
		irs.append(env["pull_value"](sm_id,"get_imu")[0])

		if abs(current_orientation - one_eight_deg) < 5:
			break

	time.sleep(1)
	orient_most_dist = orients[irs.index(max(irs))] 
	turn_to_orient(act, env, orient_most_dist, 20)
	time.sleep(5)

explore_state = State(explore_body, no_propagators)
# explore_propagators = [go_to_ready, go_to_avoid_wall]