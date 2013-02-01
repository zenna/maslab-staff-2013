from common import *
from state_machine import *
from pid import *

def ball_present(x,y):
    if abs(x - 0.0) < 0.001 and abs(y - 0.0) < 0.001:
        return True
    else:
        return False
    
#State :  explore, look for balls
def explore_body(global_mem, local_mem, act, env, check_props):
    # Do one full revolution using IMU
    print "Exploring"
    # Randomise turn left or right
    initial_speed = 30
    if random.randrange(2) == True:
        initial_speed = -initial_speed
    act["motor_left"].setSpeed(initial_speed)
    act["motor_right"].setSpeed(-initial_speed)

    start_time = time.time()

    irs = []
    time_elapses = []

    sweeps = 0
    while True:
        # Check props
        do_transition, to_where = check_props(global_mem, env)
        if do_transition == True:
            return do_transition, to_where

        sm_id = env["sync_value"]["state_machine_id"]
        img_thresh = env["pull_value"](sm_id, "img")
        x,y = find_centroid(img_thresh,  global_mem["cam_width"],  global_mem["cam_height"],  global_mem["indices_x"],  global_mem["indices_y"])

        if 370 < y < 450:
            initial_speed *= int(initial_speed * -0.8)
            act["motor_left"].setSpeed(initial_speed)
            act["motor_right"].setSpeed(-initial_speed)
            sweeps += 1
            if sweeps > 3:
                time.sleep(.5)
                roller_on(act)
                go_fwd(act, 30)
                time.sleep(2)
                stop_wheels(act)
                roller_off(act)
                return True, "explore"

        time_elapse = time.time() - start_time
        ir = env["pull_value"](sm_id, "get_ir")[0]
        irs.append(ir)
        time_elapses.append(time_elapses)

        if time_elapse > 50:
            break

    #Go back to place of farthest wall
    act["motor_left"].setSpeed(-initial_speed)
    act["motor_right"].setSpeed(initial_speed)
    time.sleep(time_elapses[irs.index(min(irs))])
    
    # Then go forward
    act["motor_left"].setSpeed(initial_speed)
    act["motor_right"].setSpeed(initial_speed)
    stop_wheels(act)
    time.sleep(
        )

    return False, None

#State :  explore, look for balls
def explore_pid_body(global_mem, local_mem, act, env, check_props):
    # Do one full revolution using IMU
    time_current = time.time() - global_mem["start_time"]
    print "exploring"
    img_thresh = env["sync_value"]["img"]

    x,y = find_centroid(img_thresh,  global_mem["cam_width"],  global_mem["cam_height"],  global_mem["indices_x"],  global_mem["indices_y"])
    # print "Centroid:", x,y
    # draw_crosshairs(x,y, img_thresh)

    past_errors = global_mem["past_errors"]
    error_current = position_error(x,y)
    np.roll(past_errors['errors'],-1)
    np.roll(past_errors['timestamps'],-1)
    past_errors['errors'][-1] = error_current
    past_errors['timestamps'][-1] = time_current
    derivative_out = find_deriviative(past_errors)
    integral_out = integrate_errors(past_errors)
    controller_out = global_mem["proportional_gain"] * error_current + global_mem["integral_gain"] * integral_out + global_mem["derivative_gain"] * derivative_out
    controller_out = int(controller_out)
    print "CONTROLLER_OUT", controller_out
    # controller_out = 0
    # print "PID", controller_out, error_current, integral_out, derivative_out
    move_differential(controller_out,global_mem, act)

    return False, None

def ball_in_sight(global_memory, local_memory, rcvd_msg, env): 
    if time.time() - global_mem["start_time"] > 30:
        return True
    else:
        return False

find_ball_prop = [{'proposition':am_init, 'dst_state_id':"explore"}]
find_ball_state = State(explore_body,find_ball_prop)
explore_state = State(explore_body, [] )
# explore_propagators = [go_to_ready, go_to_avoid_wall]