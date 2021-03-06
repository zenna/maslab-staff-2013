import numpy as np
import random
import time

import billy
from state_machine import *
from thalamus import *
from thalamic_modules import *
from states import ready_state, explore_state, fire_cannon_states, end_state, avoidwalls_state

if __name__ == "__main__":
	b4 = billy.Billy()	
	b4.init_arduino() #Get serial port for attiny
	# b4.init_windows()

	# b4.disable_motors()

	camera_id = int(sys.argv[1])
	b4.init_camera(camera_id) # Camera id is typically 1
	# b4.create_histogram()

	# A state machine could have a number of slots it can write to
	# and these slots are mapped by a separate process to an actuator
	actuators = {"motor_left": b4.motor_left, "motor_right": b4.motor_right, "roller": b4.roller, "latch": b4.latch, "spool": b4.spool}
	wheel_controllers = StateMachine(actuators)

	rs = ready_state.ready_state
	if len(sys.argv) >= 3:
		rs.propagators = [{'proposition':ready_state.ready_prop, 'dst_state_id':sys.argv[2]}]

	wheel_controllers.add_state(end_state.end_state, "end")
	wheel_controllers.add_state(rs, "ready")
	wheel_controllers.add_state(explore_state.find_ball_state, "find_ball")
	wheel_controllers.add_state(explore_state.explore_state, "explore")
	wheel_controllers.add_state(fire_cannon_states.ready_shoot_state, "ready_shoot")	
	wheel_controllers.add_state(fire_cannon_states.shoot_state, "shoot")
	wheel_controllers.add_state(avoidwalls_state.avoid_wall_state, "avoid_walls")

	wheel_controllers.set_current_state("ready")

	# cannon_controllers = StateMachine(actuators)
	# wheel_controllers.add_state(ready_state.ready_state, "ready")
	# wheel_controllers.add_state(explore_state.explore_state, "explore")
	# wheel_controllers.set_current_state("ready")


	thalamus = ThalamicNetwork()

	thalamus.add_modulator(b4.get_ir, "get_ir")
	if b4.in_red_mode() == True:
		thalamus.add_modulator(threshold_red_balls, "threshold_green_balls")
	else:
		thalamus.add_modulator(threshold_green_balls, "threshold_green_balls")

	thalamus.add_modulator(b4.get_frame, "get_frame")
	thalamus.add_modulator(bgr_to_hsv, "bgr_to_hsv")
	thalamus.add_modulator(b4.do_reset, "do_reset")
	thalamus.add_modulator(b4.in_red_mode, "in_red_mode")
	thalamus.add_modulator(b4.get_imu, "get_imu")
	thalamus.add_modulator(b4.high_button.getValue, "high_button")
	thalamus.add_modulator(b4.ir_ball.getValue, "ir_ball")
	thalamus.add_state_machine(wheel_controllers, "wheel_controllers")

	thalamus.link_nodes("get_frame", "bgr_to_hsv", "img")
	thalamus.link_nodes("bgr_to_hsv", "threshold_green_balls", "img")
	thalamus.link_nodes("threshold_green_balls", "wheel_controllers", "img")
	thalamus.link_nodes("get_ir", "wheel_controllers", "get_ir")
	thalamus.link_nodes("get_imu", "wheel_controllers", "get_imu")
	thalamus.link_nodes("do_reset", "wheel_controllers", "do_reset")
	thalamus.link_nodes("in_red_mode", "wheel_controllers", "in_red_mode")
	thalamus.link_nodes("ir_ball", "wheel_controllers", "ir_ball")
	thalamus.link_nodes("high_button", "wheel_controllers", "high_button")
	thalamus.link_nodes("get_frame", "wheel_controllers", "frame")


	try:
		thalamus.run_serial()
	except ():
	    b4.motor_left.setSpeed(0)
	    b4.motor_right.setSpeed(0)
	    b4.spool.setSpeed(0)
	    b4.latch.setAngle(90)
	    cv.DestroyAllWindows()
	    exit()
	    raise