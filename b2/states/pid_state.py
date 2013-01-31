## Seek a ball in view
from pid import *

# State: seek balls
def seek_ball_state(global_memory, local_memory, act, env):
	#Calculate motor out with PID controller
	error_current = position_error(x,y)
	np.roll(global_mem["past_errors"]['errors'],-1)
	np.roll(global_mem["past_errors"]['timestamps'],-1)
	global_mem["past_errors"]['errors'][-1] = error_current
	global_mem["past_errors"]['timestamps'][-1] = time_current
	derivative_out = find_deriviative(past_errors)
	integral_out = integrate_errors(past_errors)
	controller_out = proportional_gain * error_current + integral_gain * integral_out + derivative_gain * derivative_out
	move_differential(controller_out, act)