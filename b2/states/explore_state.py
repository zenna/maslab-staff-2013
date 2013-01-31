from common import *
from state_machine import *

#State :  explore, look for balls
def explore_body(global_memory, local_memory, act, env):
	# Do one full revolution using IMU
	print "exploring"
	id = env["sync_value"]["state_machine_id"]
	current_orientation = env["pull_value"](env.id,"get_ir")
	import ipdb
	ipdb.set_trace()
	turn_left(act, 30)
	# while True:

	# 	go_to_state.
	# 	if helpers.check_propositions() == True:
	# 		return
	# 	if done_full_circle
	# 		break

	# stop_wheels(act)

explore_state = State(explore_body, no_propagators)
# explore_propagators = [go_to_ready, go_to_avoid_wall]