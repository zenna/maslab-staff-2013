# This is the main class for the FSM

# A logical prnetwork consists of a set of states and transitions
# Two processes continue in parallel
# a - updating the environment variable from sensor data
# b - executing the current state
# c - evaluating transition functions and transitioning state
class Logical_Network:
	# States are (impure)s ctions which map the environment to true or false
	transitions = []

	def __self(): 
		# This is a constructor

	def init_arduino():
		import arduino
		ard = arduino.Arduino()
		m0 = arduino.Motor(ard, 0, 42, 9)
		m1 = arduino.Motor(ard, 0, 48, 8)
		a0 = arduino.AnalogInput(ard, 0)  # Create an analog sensor on pin A0

		ard.run()  # Start the Arduino communication thread

	def add_state(state,utility):

	def add_transition(src_state,dst_state,proposition,weight)


def rotate(world):
	world.m0.setSpeed(30)
	world.m1.setSpeed(-30)
	time.sleep(2)
	world.m0.setSpeed(0)
	world.m1.setSpeed(0)

if __name__ == "__main__":
	brain = Logical_Network()
	brain.add_state(rotate)
