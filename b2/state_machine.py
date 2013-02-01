import sys
import billy
from collections import defaultdict

# How to do things that require a time delay, without blocking everything else
# How to return to inital state
# How to implement memory, for PID controller

# How to paramterise these things for learning

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
		self.global_memory = {}

	def add_state(self, state, state_id):
		state.id = state_id
		self.states[state_id] = state

		# Store a reference in each state to its parent
		state.state_machine = self

	def set_current_state(self, state_id):
		if state_id in self.states:
			self.current_state_id = state_id
		else:
			print "ERROR: state", state_id, " non-existent"

	def add_child(self, src_state_id,dst_state_id,proposition):
		# FIX
		self.children[src_state_id].append({"dst_state_id":dst_state_id,"proposition":proposition})

	def step(self, env):
		if 	self.current_state_id == None:
			print "NO CURRENT STATE"
			return
		
		# self.states[self.current_state_id].init()
		current_state = self.states[self.current_state_id]
		try:
			do_transition, dst_state_id = current_state.code(self.global_memory, current_state.memory, self.actuators, env, current_state.check_propagations)
			
			# A state may tell you directly to transition to anotehr state
			if do_transition == True:
				self.switch_states(self.current_state_id, dst_state_id)
			else:
				do_transition, dst_state_id = current_state.check_propagations(self.global_memory, env)
				if do_transition == True:
					print "doing transition:",self.current_state_id,dst_state_id 
					self.switch_states(self.current_state_id, dst_state_id)
		except:
			pass

	def switch_states(self, current_state_id, next_state_id):
		self.global_memory["previous_state"] = current_state_id
		self.current_state_id = next_state_id
		self.states[next_state_id].rcvd_msg = self.states[current_state_id].memory

class State:
	def __init__(self, code, propagators):
		self.memory = {}
		self.rcvd_msg = {}
		self.propagators = propagators
		self.code = code

	def add_propagator(self, propagator):
		propagators.append(propagator)

	def check_propagations(self, global_memory, env):
		for propagator in self.propagators:
			# import ipdb
			# ipdb.set_trace()
			make_transition = propagator['proposition'](global_memory, self.memory, self.rcvd_msg, env)
			if make_transition == True:
				return True, propagator['dst_state_id']

		return False, self.id