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
    sm_id = env["sync_value"]["state_machine_id"]
    img_thresh = env["pull_value"](sm_id, "img")

    # Randomise turn left or right
    initial_speed = 30
    if random.randrange(2) == True:
        initial_speed = -initial_speed
    act["motor_left"].setSpeed(initial_speed)
    act["motor_right"].setSpeed(-initial_speed)

    start_time = time.time()

    irs = []
    time_elapses = []

    while True:
        # Check props
        do_transition, to_where = check_props()
        if do_transition == True:
            return do_transition, to_where

        time_elapse = time.time() - start_time
        ir = env["pull_value"](sm_id, "ir")[0]
        irs.append(ir)
        time_elapses.append(time_elapses)

        if time_elapse > 10:
            break

    #Go back to place of farthest wall
    act["motor_left"].setSpeed(-initial_speed)
    act["motor_right"].setSpeed(initial_speed)
    time.sleep(time_elapses[irs.index(min(items))])
    
    # Then go forward
    act["motor_left"].setSpeed(initial_speed)
    act["motor_right"].setSpeed(initial_speed)
    stop_wheels(act)

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

find_ball_prop = [{'proposition':am_init, 'dst_state_id':"explore"}]
find_ball_state = State(explore_body,find_ball_prop)
explore_state = State(explore_body, [] )
# explore_propagators = [go_to_ready, go_to_avoid_wall]