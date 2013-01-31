from common import *
from state_machine import *

#State :  explore, look for balls
def explore_body(global_memory, local_memory, act, env):
	# Do one full revolution using IMU
	print "exploring"
	sm_id = env["sync_value"]["state_machine_id"]
	current_orientation = env["pull_value"](sm_id,"get_imu")[3]
	turn_left(act, 30)
	while True:
		new_orient = env["pull_value"](sm_id,"get_imu")[3]
		if abs(old_orient - new_orient) < 20:
			stop_wheels(act)
			time.sleep(5)
			break

explore_state = State(explore_body, no_propagators)
# explore_propagators = [go_to_ready, go_to_avoid_wall]