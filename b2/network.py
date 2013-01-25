import networkx as nx
import sys

# This is the main class for the FSM

# A logical prnetwork consists of a set of states and transitions
# Two processes continue in parallel
# a - updating the environment variable from sensor data
# b - executing the current state
# c - evaluating transition functions and transitioning state
class StateMachine:
	# States are (impure)s ctions which map the environment to true or false
	transitions = []

	def add_state(state):
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
	billy = Billy()
	billy.init_attiny(sys.argv[0])
	billy.init_camera(1)

	thalamus = ThalamicNetwork()
	thalamus.add_module(shrink_camera)
	thalamus.add_module(threshold_green_balls)
	thalamus.link_modules(bgr_to_hsv, threshold_green_balls)
	thalamus.add_module(billy.get_frame)
	thalamus.link_modules(billy.get_frame, bgr_to_hsv)