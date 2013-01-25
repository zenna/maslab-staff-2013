ismport networkx as nx
import sys

# This is the main class for the FSM

# A logical prnetwork consists of a set of states and transitions
# Two processes continue in parallel
# a - updating the environment variable from sensor data
# b - executing the current state
# c - evaluating transition functions and transitioning state
class StateMachine:

	# States are (impure)s ctions which map the environment to true or false
	def __init__(self):
		self.graph = nx.DiGraph()
		self.current_state = None

	def add_state(state):
		pass

	def add_transition(src_state,dst_state,proposition,weight):
		pass
     

class ThalamicNetwork:
	def __init__(self):
		self.graph = nx.DiGraph()

	def add_state_machine(state_machine):
		network.add_node(state_machine)

	def add_module(module):
		network.add_node(module)

	def link_modules(module1, module2):
		network.add_edge(module1, module2)

	def update_state_machine_inputs():

	def modulate_state_transitions():
		for state_machine in state_machines:
			stateself.

# Reduce image size
def bgr_to_hsv(img):
	# Convert from BGR to HSV
	hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
	cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
	return hsv

def threshold_green_balls(img):
	# Threshold the img in hsv space for green
	img_thresh = cv.CreateImage(cv.GetSize(img), 8, 1)
	cv2.cv.InRangeS(hsv, cv.Scalar(180*145/360, 100, 84), cv.Scalar(180*165/360, 220, 255), img_thresh)
	return img_thresh

# def pid_integrate_init():
# 	#PID controller, tuning params:
# 	proportional_gain = .2
# 	integral_gain = .01
# 	derivative_gain = 2

# 	window_size = 1000
# 	past_errors = {'errors':np.zeros([window_size]),'timestamps':np.zeros([window_size])}

# def pid_integrate():
# 	# Calculate motor out with PID controller
# 	x,y = find_centroid(img_thresh, billy.cam_width, billy.cam_height)
# 	error_current = position_error(x,y)
# 	np.roll(past_errors['errors'],-1)
# 	np.roll(past_errors['timestamps'],-1)
# 	past_errors['errors'][-1] = error_current
# 	past_errors['timestamps'][-1] = time_current
# 	derivative_out = find_deriviative(past_errors)
# 	integral_out = integrate_errors(past_errors)
# 	controller_out = proportional_gain * error_current + integral_gain * integral_out + derivative_gain * derivative_out
# 	billy.single_value_move(controller_out)

def go_fwd():
	motor_left.setSpeed(100)
	motor_right.setSpeed(100)

def go_bckwd():
	motor_left.setSpeed(100)
	motor_right.setSpeed(-100)

def time_is_even():
	if int(time) % 20 == 0:
		return True
	else:
		return False

if __name__ == "__main__":
	billy = Billy()
	billy.init_attiny(sys.argv[0]) #Get serial port for attiny
	billy.init_camera(1) # Camera id is typically 1

	# wheel_controllers = StateMachine(proportional_gain, integral_gain, derivative_gain, window_size, past_errors)
	# wheel_controllers.add_state(pid_integrate)

	wheel_controllers = StateMachine()
	wheel_controllers.add_state(go_fwd)
	wheel_controllers.add_state(go_bckwd)
	wheel_controllers.add_transition(go_fwd,go_bckwd, time_is_even)

	thalamus = ThalamicNetwork()

	thalamus.add_module(billy.get_ir)
	thalamus.add_module(threshold_green_balls)
	thalamus.add_module(billy.get_frame)
	thalamus.add_module(billy.bgr_to_hsv)
	thalamus.add_module(wheel_controllers)

	thalamus.link_modules(billy.get_frame, bgr_to_hsv)
	thalamus.link_modules(bgr_to_hsv, threshold_green_balls)
	thalamus.link_modules(threshold_green_balls, wheel_controllers)