from collections import defaultdict

class ThalamicNetwork:
	def __init__(self):
		self.state_machines = {}
		self.modulators = {}
		self.parents = defaultdict(list)

	def add_state_machine(self, state_machine, state_machine_id):
		self.state_machines[state_machine_id] = state_machine

		# Store a reference in each state to its parent
		state_machine.thalamic_network = self

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

	def pull_value(self, state_machine_id, arg_name):
		for parent in self.parents[state_machine_id]:
			if parent["dst_arg_name"] == arg_name:
				value = self.evaluate_modulator(parent["src_node_id"])
				return value
		print "ERROR, PULL FAILED"
		return None

	def update_state_machine_inputs(self):
		#Synchronously update all inputs to statemachnes
		temp_current_values = defaultdict(dict)
		for state_machine_id in self.state_machines.keys():
			for parent in self.parents[state_machine_id]:
				value = self.evaluate_modulator(parent['src_node_id'])
				temp_current_values[state_machine_id][parent['dst_arg_name']] = value
				#Kind of hack to be able to pull values
				# temp_current_values[state_machine_id]["pull"] = self.pull_value

		self.current_values = temp_current_values

	def run_serial(self):
		# A serial (not parallel) version of main loop to run
		# In sequence we update input to state machines
		# Perform state machine transitions
		# run state machines
		env = {"pull":self.pull_value}
		while True:
			self.update_state_machine_inputs()
			for state_machine_id, state_machine in self.state_machines.items():
				#Step state machine with the current values from thalamic network
				env["sync_value"] = self.current_values[state_machine_id]
				state_machine.step(env)
