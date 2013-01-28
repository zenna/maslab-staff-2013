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
		# States is a set of functions
		self.states = {}

		# Stores edges, is a map from a state_id
		# to a list of pairs: [child_id, proposition]
		self.children = {}
		self.current_state_id = None

	def add_state(self, state, state_id):
		self.states[state_id] = state 

	def set_current_state(state_id):
		if state_id in self.states:
			self.current_state = state_id
		else:
			print "ERROR: state", state_id, " non-existent"

	def add_child(src_state_id,dst_state_id,proposition,weight):
		# FIX
		self.children[src_state_id].append([dst_state_id,proposition)]

	def check_propositions(self, state_id):
		# This checks all propositions to all children
		# of state id, and returns the state to transition
		# to if any are false, otherwise returns originala state
		for child in self.children[state_id]:
			do_transition = child[0]()
			if do_transition == True:
				return child[1]

		return state_id

	def step(self, env, act):
		if 	self.current_state_id = None:
			print "NO CURRENT STATE"
			return
		
		check_propositions(current_state_id)
		current_state(env, act)
     
class ThalamicNetwork:
	def __init__(self):
		self.state_machines = []
		self.modulators = {}
		self.parents = {}
		self.state_machine_inputs_now = {}

	def add_state_machine(state_machine, state_machine_id):
		self.state_machines[state_machine_id] = state_machine
		self.state_machine_inputs_now[state_machine_id] = {}

	def add_modulator(modulator, modulator_id):
		self.modulators[modulator_id] = modulator

	def link_nodes(src_node_id, dst_node_id, dst_arg_name):
		#FIX APPEND
		self.parents[dst_node_id].append({"src_node_id":src_node_id, "dst_arg_name":dst_arg_name})

	def evaluate_modulator(modulator_id):
		# Recursive function which evaluates functional tree of modulators
		kwargs = {}

		# First find values of all arguments for modulator_id function by
		# recursion.  Recursion stops when we reach a function of no arguments
		# e.g. a value from the camera
		for parent in self.parents[modulator_iwd]:
			kwargs[parent["dst_arg_name"]] = evaluate_modulator(parent['src_node_id'])

		# Then call this function with arguments, 
		return self.modulators[modulator_id](**kwargs)

	def update_state_machine_inputs():
		#Synchronously update all inputs to statemachnes
		temp_current_values = {}
		for state_machine_id in state_machines.keys():
			for parent in self.parents[state_machine_id]:
				value = evaluate_modulator(parent['dst_arg_name'])
				temp_current_values['state_machine_id']['arg_name'] = value

		self.current_values = temp_current_values

	def run_serial():
		# A serial (not parallel) version of main loop to run
		# In sequence we update input to state machines
		# Perform state machine transitions
		# run state machines
		while True:
			update_state_machine_inputs()
			for state_machine in state_machines:
				state_machines.step()

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

def go_fwd(env,act):
	print "going fwd"
	act.motor_left.setSpeed(100)
	act.motor_right.setSpeed(100)

def go_bckwd(env,act):
	print "going bckwd"
	act.motor_left.setSpeed(100)
	act.motor_right.setSpeed(-100)

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
	wheel_controllers.add_state(go_fwd, "go_fwd")
	wheel_controllers.add_state(go_bkwd, "go_bkwd")
	wheel_controllers.add_transition("go_fwd","go_bkwd", time_is_even)
	wheel_controllers.set_current_state("go_fwd")
	wheel_controllers.run()

	thalamus = ThalamicNetwork()

	thalamus.add_module(billy.get_ir, "get_ir")
	thalamus.add_module(threshold_green_balls, "threshold_green_balls")
	thalamus.add_module(billy.get_frame, "get_frame")
	thalamus.add_module(billy.bgr_to_hsv, "bgr_to_hsv")
	thalamus.add_module(wheel_controllers, "wheel_controllers")

	thalamus.link_modules("get_frame", "bgr_to_hsv")
	thalamus.link_modules("bgr_to_hsv", "threshold_green_balls")
	thalamus.link_modules("threshold_green_balls", "wheel_controllers")