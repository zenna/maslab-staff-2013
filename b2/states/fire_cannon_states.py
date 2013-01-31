from common import *

SPOOL_POSITION_READY = 10
SPOOL_POSITION_GRABBING = 10
UNLATCHED_ANGLE = 90

def ready_shoot_body(global_memory, local_memory, act, env):
	act.latch.set_angle(UNLATCHED_ANGLE)
	act.spool.move_to_pos(SPOOL_POSITION_GRABBING)
	act.latch.set_angle(LATCHED_ANGLE)
	act.spool.move_to_pos(SPOOL_POSITION_READY)

def ready_to_shoot(global_memory, local_memory, act, env):
	pass

def shoot_body(global_memory, local_memory, act, env):
	act.latch.set_angle(UNLATCHED_ANGLE)