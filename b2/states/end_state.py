from common import *
from state_machine import *

def end_body(global_mem, local_mem, act, env, check_props):
	print "Shutting down"
	stop_all_motors(act)
	exit()
	return False, None

end_state = State(end_body, [go_to_end])