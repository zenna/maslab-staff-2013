from common import *
from state_machine import *
from pid import *

#State :  explore, look for balls
def explore_body(global_mem, local_mem, act, env):
	# Do one full revolution using IMU
	print "exploring"
	# sm_id = env["sync_value"]["state_machine_id"]
	img_thresh = env["sync_value"]["img"]
	# img =

	x,y = find_centroid(img_thresh,  global_mem["cam_width"],  global_mem["cam_height"],  global_mem["indices_x"],  global_mem["indices_y"])
	print "Centroid:", x,y
	draw_crosshairs(x,y, img_thresh)

	if y < 330:
	    print "rotateleft"
	    act["roller"].setSpeed(0)
	    turn_left(act)
	    time.sleep(.1)
	    stop_wheels(act)
	elif y > 470:
	    print "rotateright"
	    act["roller"].setSpeed(0)
	    turn_right(act)
	    time.sleep(.1)
	    stop_wheels(act)
	else:
	    time.sleep(10)

	## OLD


	# current_orientation = env["pull_value"](sm_id,"get_imu")[0]
	# one_eight_deg = (current_orientation + 180) % 360

	# turn_to_orient(act, env, one_eight_deg, 20)

	# import ipdb
	# ipdb.set_trace()

	# turn_left(act)
	# orients = []
	# irs = []
	# while True:
	# 	env["pull_value"](sm_id,"get_imu")[0]
	# 	orients.append(env["pull_value"](sm_id,"get_imu")[0])
	# 	irs.append(env["pull_value"](sm_id,"get_imu")[0])

	# 	if abs(current_orientation - one_eight_deg) < 5:
	# 		break

	# time.sleep(1)
	# orient_most_dist = orients[irs.index(max(irs))] 
	# turn_to_orient(act, env, orient_most_dist, 20)
	# time.sleep(5)

explore_state = State(explore_body, no_propagators)
# explore_propagators = [go_to_ready, go_to_avoid_wall]