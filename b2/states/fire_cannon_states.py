from common import *
from state_machine import *

UNLATCHED_ANGLE = 50
LATCHED_ANGLE = 10
def ready_shoot_body(global_memory, local_memory, act, env):
	act["latch"].setAngle(UNLATCHED_ANGLE)
	act["spool"].setSpeed(-40)
	time.sleep(3)
	act["spool"].setSpeed(0)
	act["latch"].setAngle(LATCHED_ANGLE)
	time.sleep(1)
	act["spool"].setSpeed(100)
	time.sleep(2)
	act["spool"].setSpeed(0)
	time.sleep(.5)
	act["latch"].setAngle(UNLATCHED_ANGLE)
	time.sleep(10)
	return False, None


def ready_to_shoot(global_memory, local_memory, act, env):
	pass

def shoot_body(global_memory, local_memory, act, env):
	act["latch"].set_angle(UNLATCHED_ANGLE)

ready_shoot_state = State(ready_shoot_body, no_propagators)