from common import *
from state_machine import *

import cv2.cv as cv

## Ready State Body : initialisation and ready to go
def ready_body(global_mem, local_mem, act, env, check_props):
	# This state initialises memory and gets ready for the button press
	print "In ready state"
	stop_all_motors(act)
	if "initialised" not in local_mem:
		global_mem['start_time'] = time.time()
		#PID controller, tuning params:
		global_mem["motor_right_speed"] = 10
		global_mem["motor_left_speed"] = 10

		global_mem["proportional_gain"] = .05
		global_mem["integral_gain"] = .01
		global_mem["derivative_gain"] = 1
		window_size = 100
		global_mem["past_errors"] = {'errors':np.zeros([window_size]),'timestamps':np.zeros([window_size])}
		local_mem["initialised"] = True

		# Centroid Init
		global_mem["cam_width"] = cam_width = 640
		global_mem["cam_height"] = cam_height = 480

		# FIXME: Pobably these indices should be local memory
		global_mem["indices_x"] = np.tile(range(cam_width),[cam_height,1])
		indices_y = np.tile(range(cam_width),[cam_width,1]).transpose()
		global_mem["indices_y"] = indices_y[0:cam_height,0:cam_width]

	sm_id = env["sync_value"]["state_machine_id"]
	frame = env["pull_value"](sm_id, "img")
	img_thresh = env["pull_value"](sm_id, "frame")
	# img_thresh = env["pull_value"](sm_id, "img")

	# cv.ShowImage("camera", frame)
	# cv.ShowImage("ball", img_thresh)
	# cv.WaitKey(10)
	# cv.ShowImage("wall", self.get_frame())

	return False, None

def reset_switch_down(global_mem, local_mem, rcvd_msg, env):
	sm_id = env["sync_value"]["state_machine_id"]
	do_reset = env["pull_value"](sm_id, "do_reset")
	if do_reset == True:
		return True
	else:
		return False

def ready_prop(global_memory, local_memory, rcvd_msg, env):
	return am_init(global_memory, local_memory, rcvd_msg, env) and reset_switch_down(global_memory, local_memory, rcvd_msg, env)

def time_up_prop(global_memory, local_memory, rcvd_msg, env):
	if time.time() - global_mem["start_time"] > 30:
		return True
	else:
		return False

# ready -> explore
ready_propagators = [go_to_end, {'proposition':ready_prop, 'dst_state_id':"explore"}]
ready_state = State(ready_body, ready_propagators)