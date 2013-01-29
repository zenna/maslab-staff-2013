import sys
import billy
from collections import defaultdict

import cv2
import cv2.cv as cv
import time
import numpy as np
import random
import time

# How to do things that require a time delay, without blocking everything else
# How to return to inital state
# How to implement memory, for PID controller

# How to paramterise these things for learning
# 

# This is the main class for the FSM
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

class State:
	def __init__(self):
		self.memory = {}
		self.propogators = []
		self.code = None

	def 