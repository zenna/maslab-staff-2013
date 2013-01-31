#!/usr/bin/python

import cv2
import cv2.cv as cv
import time
import numpy
import pdb
import numpy as np
import random
import sys
sys.path.append("..")
import time
import arduino
import attiny
import scipy.integrate

from billy import *

# Calculate the centroid of an image
def find_centroid(img_c, cam_width, cam_height, indices_x, indices_y):
    img = numpy.asarray(img_c[0:cam_height,0:cam_width]) / 255.0
    total_weight = numpy.sum(img)
    x = numpy.sum(numpy.sum(img * indices_x,0))
    y = numpy.sum(numpy.sum(img * indices_y,0))
    if total_weight != 0:
        x /= total_weight
        y /= total_weight
    return y,x

# Draw crosshairs onto img
def draw_crosshairs(x,y, img):
    import random
    holder = x
    x = int(y)
    y = int(holder)
    icolor = random.randint(0, 0xFFFFFF)
    colour = cv.Scalar(icolor & 0xff, (icolor >> 8) & 0xff, (icolor >> 16) & 0xff)
    halfwidth = 10
    line_type = cv.CV_AA
    #TODO check line is within image
    pt1 = (x-halfwidth,y)
    pt2 = (x+halfwidth,y)
    cv.Line(img, pt1, pt2,
               colour,
               random.randrange(0, 10),
               line_type, 0)
    
    cv.Line(img, (x,y-halfwidth), (x,y+halfwidth),
               colour,
               random.randrange(0, 10),
               line_type, 0)

# error is distan   ce of centroid from centre of vision
def position_error(x,y):
    return y - 500

def integrate_errors(past_errors):
    integral = scipy.integrate.trapz(past_errors['errors'], past_errors['timestamps'])
    return integral

def find_deriviative(past_errors):
    return (past_errors['errors'][-1] - past_errors['errors'][-2]) / (past_errors['timestamps'][-1] - past_errors['timestamps'][-2])


if __name__ == "__main__":

    billy = Billy()
    # billy.init_attiny("/dev/serial/by-id/usb-FTDI_TTL232R_FTFBGOT5-if00-port0")
    billy.init_camera(1)
    billy.init_arduino()

    # Indices used for calculating the centroid
    indices_x = numpy.tile(range(billy.cam_width),[billy.cam_height,1])
    indices_y = numpy.tile(range(billy.cam_width),[billy.cam_width,1]).transpose()
    indices_y = indices_y[0:billy.cam_height,0:billy.cam_width]

    #PID controller, tuning params:
    proportional_gain = 1
    integral_gain = 1
    derivative_gain = 1

    from getch import Getch
    gch = Getch()

    window_size = 1000
    past_errors = {'errors':np.zeros([window_size]),'timestamps':np.zeros([window_size])}

    zero_time = time.time()
    # while True:
    # 	print "waiting"
    # 	if billy.do_reset() == True:
    # 		break

    try:
        while True:
            img = billy.get_frame()

            time_current = time.time() - zero_time

            print "times", zero_time, time_current

            # Convert from BGR to HSV
            hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
            cv.CvtColor(img, hsv, cv.CV_BGR2HSV)

            # Threshold the img in hsv space for green
            img_thresh = cv.CreateImage(cv.GetSize(img), 8, 1)

            if billy.in_red_mode() == True:
            	cv2.cv.InRangeS(hsv, cv.Scalar(0, 100, 166), cv.Scalar(25, 220, 192), img_thresh)
            else:
            	cv2.cv.InRangeS(hsv, cv.Scalar(180*145/360, 100, 84), cv.Scalar(180*165/360, 220, 255), img_thresh)

            # Find the centroid of the image
            x,y = find_centroid(img_thresh, billy.cam_width, billy.cam_height, indices_x, indices_y)
        
            print "CENTROID", x,y
            draw_crosshairs(x,y, img_thresh)

            # Calculate motor out with PID controller
            error_current = position_error(x,y)
            np.roll(past_errors['errors'],-1)
            np.roll(past_errors['timestamps'],-1)
            past_errors['errors'][-1] = error_current
            past_errors['timestamps'][-1] = time_current
            derivative_out = find_deriviative(past_errors)
            integral_out = integrate_errors(past_errors)

            controller_out = proportional_gain * error_current + integral_gain * integral_out + derivative_gain * derivative_out
            billy.single_value_move(controller_out)

            # if y < 330:
            #     print "rotateleft"
            #     billy.roller.setSpeed(0)
            #     billy.motor_right.setSpeed(20)
            #     billy.motor_left.setSpeed(-20)
            #     time.sleep(.1)
            #     billy.motor_right.setSpeed(0)
            #     billy.motor_left.setSpeed(0)
            # elif y > 470:
            #     print "rotateright"
            #     billy.roller.setSpeed(0)
            #     billy.motor_right.setSpeed(-20)
            #     billy.motor_left.setSpeed(20)
            #     time.sleep(.1)
            #     billy.motor_right.setSpeed(0)
            #     billy.motor_left.setSpeed(0)
            # else:
            #     print "frws"
            #     billy.roller.setSpeed(-126)
            #     billy.motor_right.setSpeed(30)
            #     billy.motor_left.setSpeed(30)
            #     time.sleep(1)

            if time_current > 5:
                billy.motor_right.setSpeed(0)
                billy.motor_left.setSpeed(0)
                char = gch()
                if char == "q":
                    proportional_gain *= 1.1
                elif char == "w":
                    integral_gain *= 1
                elif char == "e":
                    derivative_gain *= 1.1
                elif char == "a":
                    proportional_gain *= .9
                elif char == "s":
                    integral_gain *= .9
                elif char == "d":
                    derivative_gain *= .9
                zero_time = time.time() 

            print "GAINS", proportional_gain, derivative_gain, integral_gain

            cv.ShowImage("threshholded", img_thresh  )
            cv.ShowImage("camera", img  )   
            if cv.WaitKey(10) == 27:
                break
    except ():
        billy.motor_left.setSpeed(0)
        billy.motor_right.setSpeed(0)
        cv.DestroyAllWindows()
        raise
    cv.DestroyAllWindows()
