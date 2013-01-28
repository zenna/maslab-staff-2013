import sys
import billy
from collections import defaultdict

import cv2
import cv2.cv as cv
import time
import numpy as np
import random
import time

# This is the main class for the FSM

# A logical prnetwork consists of a set of states and transitions
# Two processes continue in parallel
# a - updating the environment variable from sensor data
# b - executing the current state
# c - evaluating transition functions and transitioning state
class StateMachine:
	# States are (impure)s ctions which map the environment to true or false
	def __init__(self, actuators):
		# States is a set of functions
		self.states = {}
		self.actuators = actuators
		# Stores edges, is a map from a state_id
		# to a list of pairs: [child_id, proposition]
		self.children = defaultdict(list)
		self.current_state_id = None

	def add_state(self, state, state_id):
		self.states[state_id] = state 

	def set_current_state(self, state_id):
		if state_id in self.states:
			self.current_state_id = state_id
		else:
			print "ERROR: state", state_id, " non-existent"

	def add_child(self, src_state_id,dst_state_id,proposition):
		# FIX
		self.children[src_state_id].append({"dst_state_id":dst_state_id,"proposition":proposition})

	def check_propositions(self, state_id, env):
		# This checks all propositions to all children
		# of state id, and returns the state to transition
		# to if any are true, otherwise returns original state
		for child in self.children[state_id]:
			do_transition = child["proposition"](**env)
			if do_transition == True:
				return child["dst_state_id"]

		return state_id

	def step(self, env):
		if 	self.current_state_id == None:
			print "NO CURRENT STATE"
			return
		
		new_state = self.check_propositions(self.current_state_id, env)
		self.set_current_state(new_state)
		self.states[self.current_state_id](self.actuators, **env)

#TODO, FIX MAIN
# FIX APPEND PROBLEMS
# HOW DO states access environment
     
class ThalamicNetwork:
	def __init__(self):
		self.state_machines = {}
		self.modulators = {}
		self.parents = defaultdict(list)

	def add_state_machine(self, state_machine, state_machine_id):
		self.state_machines[state_machine_id] = state_machine

	def add_modulator(self, modulator, modulator_id):
		self.modulators[modulator_id] = modulator

	def link_nodes(self, src_node_id, dst_node_id, dst_arg_name):
		self.parents[dst_node_id].append({"src_node_id":src_node_id, "dst_arg_name":dst_arg_name})

	def evaluate_modulator(self, modulator_id):
		# Recursive function which evaluates functional tree of modulators
		kwargs = {}

		# First find values of all arguments for modulator_id function by
		# recursion.  Recursion stops when we reach a function of no arguments
		# e.g. a value from the camera
		for parent in self.parents[modulator_id]:
			kwargs[parent["dst_arg_name"]] = self.evaluate_modulator(parent['src_node_id'])

		# Then call this function with arguments, 
		return self.modulators[modulator_id](**kwargs)

	def update_state_machine_inputs(self):
		#Synchronously update all inputs to statemachnes
		temp_current_values = defaultdict(dict)
		for state_machine_id in self.state_machines.keys():
			for parent in self.parents[state_machine_id]:
				value = self.evaluate_modulator(parent['src_node_id'])
				temp_current_values[state_machine_id][parent['dst_arg_name']] = value

		self.current_values = temp_current_values

	def run_serial(self):
		# A serial (not parallel) version of main loop to run
		# In sequence we update input to state machines
		# Perform state machine transitions
		# run state machines
		while True:
			self.update_state_machine_inputs()
			for state_machine_id, state_machine in self.state_machines.items():
				#Step state machine with the current values from thalamic network
				state_machine.step(self.current_values[state_machine_id])

# Reduce image size
def bgr_to_hsv(img):
	# Convert from BGR to HSV
	hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
	cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
	return hsv

def threshold_green_balls(img):
	# Threshold the img in hsv space for green
	img_thresh = cv.CreateImage(cv.GetSize(img), 8, 1)
	cv2.cv.InRangeS(img, cv.Scalar(180*145/360, 100, 84), cv.Scalar(180*165/360, 220, 255), img_thresh)
	return img_thresh

def go_fwd(act,img):
	print "going fwd"
	# act.motor_left.setSpeed(100)
	# act.motor_right.setSpeed(100)

def go_bkwd(act,img):
	print "going bckwd"
	# act.motor_left.setSpeed(100)
	# act.motor_right.setSpeed(-100)

def time_is_even(img):
	now = time.time()
	if int(now) % 20 == 0:
		return True
	else:
		return False

if __name__ == "__main__":


	b4 = billy.Billy()
	b4.init_arduino() #Get serial port for attiny
	b4.init_camera(0) # Camera id is typically 1

	# A state machine could have a number of slots it can write to
	# and these slots are mapped by a separate process to an actuator
	actuators = {"motor_left": b4.motor_left, "motor_right": b4.motor_right}
	wheel_controllers = StateMachine(actuators)
	wheel_controllers.add_state(go_fwd, "go_fwd")
	wheel_controllers.add_state(go_bkwd, "go_bkwd")
	wheel_controllers.add_child("go_fwd","go_bkwd", time_is_even)
	wheel_controllers.set_current_state("go_fwd")

	thalamus = ThalamicNetwork()

	thalamus.add_modulator(b4.get_ir, "get_ir")
	thalamus.add_modulator(threshold_green_balls, "threshold_green_balls")
	thalamus.add_modulator(b4.get_frame, "get_frame")
	thalamus.add_modulator(bgr_to_hsv, "bgr_to_hsv")
	thalamus.add_state_machine(wheel_controllers, "wheel_controllers")

	thalamus.link_nodes("get_frame", "bgr_to_hsv", "img")
	thalamus.link_nodes("bgr_to_hsv", "threshold_green_balls", "img")
	thalamus.link_nodes("threshold_green_balls", "wheel_controllers", "img")

	thalamus.run_serial()