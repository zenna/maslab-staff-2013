from common import *
from state_machine import *
from pid import *

#State :  explore, look for balls
def explore_body(global_mem, local_mem, act, env):
    # Do one full revolution using IMU
    print "exploring"
    # sm_id = env["sync_value"]["state_machine_id"]
    img_thresh = env["sync_value"]["img"]
    # img =

    x,y = find_centroid(img_thresh,  global_mem["cam_width"],  global_mem["cam_height"],  global_mem["indices_x"],  global_mem["indices_y"])
    print "Centroid:", x,y
    draw_crosshairs(x,y, img_thresh)

    if y < 330:
        print "rotateleft"
        act["roller"].setSpeed(0)
        turn_left(act,25)
        time.sleep(.1)
        stop_wheels(act)
    elif y > 470:
        print "rotateright"
        act["roller"].setSpeed(0)
        turn_right(act,25)
        time.sleep(.1)
        stop_wheels(act)
    else:
        local_mem["initialised"] = True
        time.sleep(2)

#State :  explore, look for balls
def explore_pid_body(global_mem, local_mem, act, env):
    # Do one full revolution using IMU
    time_current = time.time() - global_mem["start_time"]
    print "exploring"
    img_thresh = env["sync_value"]["img"]

    x,y = find_centroid(img_thresh,  global_mem["cam_width"],  global_mem["cam_height"],  global_mem["indices_x"],  global_mem["indices_y"])
    print "Centroid:", x,y
    draw_crosshairs(x,y, img_thresh)

    past_errors = global_mem["past_errors"]
    error_current = position_error(x,y)
    np.roll(past_errors['errors'],-1)
    np.roll(past_errors['timestamps'],-1)
    past_errors['errors'][-1] = error_current
    past_errors['timestamps'][-1] = time_current
    derivative_out = find_deriviative(past_errors)
    integral_out = integrate_errors(past_errors)
    # controller_out = global_mem["proportional_gain"] * error_current + global_mem["integral_gain"] * integral_out + global_mem["derivative_gain"] * derivative_out
    controller_out = 0
    # print "PID", controller_out, error_current, integral_out, derivative_out
    move_differential(controller_out,global_mem, act)

def explore_compass_body(global_mem, local_mem, act, env):
    pass
    # current_orientation = env["pull_value"](sm_id,"get_imu")[0]
    # one_eight_deg = (current_orientation + 180) % 360

    # turn_to_orient(act, env, one_eight_deg, 20)

    # import ipdb
    # ipdb.set_trace()

    # turn_left(act)
    # orients = []
    # irs = []
    # while True:
    #   env["pull_value"](sm_id,"get_imu")[0]
    #   orients.append(env["pull_value"](sm_id,"get_imu")[0])
    #   irs.append(env["pull_value"](sm_id,"get_imu")[0])

    #   if abs(current_orientation - one_eight_deg) < 5:
    #       break

    # time.sleep(1)
    # orient_most_dist = orients[irs.index(max(irs))] 
    # turn_to_orient(act, env, orient_most_dist, 20)
    # time.sleep(5)

find_ball_prop = [{'proposition':am_init, 'dst_state_id':"explore"}]
find_ball_state = State(explore_body,find_ball_prop)
explore_state = State(explore_pid_body, no_propagators)
# explore_propagators = [go_to_ready, go_to_avoid_wall]