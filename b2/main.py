import numpy as np
import random
import time

import billy
from state_machine import *
from thalamus import *
from thalamic_modules import *
from states import ready_state, explore_state

if __name__ == "__main__":
	b4 = billy.Billy()
	b4.init_arduino() #Get serial port for attiny
	b4.disable_motors()
	b4.init_camera(0) # Camera id is typically 1

	# A state machine could have a number of slots it can write to
	# and these slots are mapped by a separate process to an actuator
	actuators = {"motor_left": b4.motor_left, "motor_right": b4.motor_right, "roller": b4.roller}
	wheel_controllers = StateMachine(actuators)
	wheel_controllers.add_state(ready_state.ready_state, "ready")
	wheel_controllers.add_state(explore_state.explore_state, "explore")
	wheel_controllers.set_current_state("ready")

	thalamus = ThalamicNetwork()

	thalamus.add_modulator(b4.get_ir, "get_ir")
	thalamus.add_modulator(threshold_green_balls, "threshold_green_balls")
	thalamus.add_modulator(b4.get_frame, "get_frame")
	thalamus.add_modulator(bgr_to_hsv, "bgr_to_hsv")
	thalamus.add_state_machine(wheel_controllers, "wheel_controllers")

	thalamus.link_nodes("get_frame", "bgr_to_hsv", "img")
	thalamus.link_nodes("bgr_to_hsv", "threshold_green_balls", "img")
	thalamus.link_nodes("threshold_green_balls", "wheel_controllers", "img")
	thalamus.link_nodes("get_ir", "wheel_controllers", "ir")

	thalamus.run_serial()