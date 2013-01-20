import networkx as nx

# This is the main class for the FSM

# A logical prnetwork consists of a set of states and transitions
# Two processes continue in parallel
# a - updating the environment variable from sensor data
# b - executing the current state
# c - evaluating transition functions and transitioning state
class Logical_Network:
	# States are (impure)s ctions which map the environment to true or false
	transitions = []

	def add_state(state,utility):
		pass

	def add_transition(src_state,dst_state,proposition,weight):
		pass

def rotate(world):
	world.m0.setSpeed(30)
	world.m1.setSpeed(-30)
	time.sleep(2)
	world.m0.setSpeed(0)
	world.m1.setSpeed(0)

class ThalamicNetwork:
	def add_module(module):
		network.add_node(module)

	def link_modules(module1, module2):
		network.add_edge(module1, module2)
 
# Reduce image size
def shrink_camera(img):
	return small_img

def threshold_green_balls(img):
	return thresholded_img

def run_brain():
	#1. Find roots
	while True:
		for root in roots:
			roots
		# First we want to get data from sensors
		# But within any particular loop we only want to get
		# This data once.
		# We also might want to give priority to other things like the IR sensor
		# Q1 which

if __name__ == "__main__":
	thalamus = ThalamicNetwork()
	thalamus.add_module(shrink_camera)
	thalamus.add_module(threshold_green_balls)
	thalamus.link_modules(shrink_camera, threshold_green_balls)

	billy = Billy()
	thalamus.add_module(billy.get_frame)
	thalamus.link_modules(billy.get_frame, shrink_camera) m,
