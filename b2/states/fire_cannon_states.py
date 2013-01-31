from common import *
from state_machine import *

UNLATCHED_ANGLE = 90
LATCHED_ANGLE = 140
def ready_shoot_body(global_memory, local_memory, act, env):
	act["latch"].set_angle(UNLATCHED_ANGLE)
	act["spool"].setSpeed(-50)
	time.sleep(1)
	act["spool"].setSpeed(0)
	act["latch"].set_angle(LATCHED_ANGLE)
	act["spool"].setSpeed(50)
	time.sleep(1.5)
	act["spool"].setSpeed(0)
	time.sleep(100)

def ready_to_shoot(global_memory, local_memory, act, env):
	pass

def shoot_body(global_memory, local_memory, act, env):
	act["latch"].set_angle(UNLATCHED_ANGLE)

ready_shoot_state = State(ready_shoot_body, no_propagators)