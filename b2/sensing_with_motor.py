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

class Billy:
    def __init__(self):
        self.cam_initialised = False
        self.arduino_initialised = False
        self.attiny_initialised = False

    def init_arduino(self):
        #setup arduino
        self.ard = arduino.Arduino()
        self.motor_right = arduino.Motor(ard, 0, 42, 9)
        self.motor_left = arduino.Motor(ard, 0, 48, 8)
        self.a0 = arduino.AnalogInput(ard, 0)  # Create an analog sensor on pin A0
        self.ard.run()  # Start the Arduino communication thread

    def init_attiny(self, port):
        #iniitalise attiny microprocessor (arduino alternative)
        self.att = attiny.ATtiny(port)
        self.motor_right = attiny.Motor(self.att, "n", "m")
        self.motor_left = attiny.Motor(self.att, "p", "o")

    def init_camera(self, camera_id):
        cam_width = self.cam_width = 640
        cam_height = self.cam_height = 480
        indices_x = numpy.tile(range(cam_width),[cam_height,1])
        indices_y = numpy.tile(range(cam_width),[cam_width,1]).transpose()
        indices_y = indices_y[0:cam_height,0:cam_width]
        cv.NamedWindow("camera", 0)
        cv.NamedWindow("threshholded", 1)
        self.capture = cv.CaptureFromCAM(camera_id)
        self.cam_initialised = True

    def get_frame(self):
        if self.cam_initialised == False:
            self.init_camera()
        return cv.QueryFrame(self.capture)

    def single_value_move(self, move):
        print "moving", move
        baseline_speed = 130
        self.motor_left.setSpeed(int(baseline_speed+move/2.))
        self.motor_right.setSpeed(int(baseline_speed-move/2.))

# Calculate the centroid of an image
def find_centroid(img_c, cam_width, cam_height):
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


# error is distance of centroid from centre of vision
def position_error(x,y):
    return y - 300

def integrate_errors(past_errors):
    integral = scipy.integrate.trapz(past_errors['errors'], past_errors['timestamps'])
    return integral


def find_deriviative(past_errors):
    return (past_errors['errors'][-1] - past_errors['errors'][-2]) / (past_errors['timestamps'][-1] - past_errors['timestamps'][-2])


if __name__ == "__main__":

    billy = Billy()
    billy.init_attiny("/dev/serial/by-id/usb-FTDI_TTL232R_FTFBGOT5-if00-port0")
    billy.init_camera(1)

    # Indices used for calculating the centroid
    indices_x = numpy.tile(range(billy.cam_width),[billy.cam_height,1])
    indices_y = numpy.tile(range(billy.cam_width),[billy.cam_width,1]).transpose()
    indices_y = indices_y[0:billy.cam_height,0:billy.cam_width]

    #PID controller, tuning params:
    proportional_gain = .2
    integral_gain = .01
    derivative_gain = 2

    window_size = 1000
    past_errors = {'errors':np.zeros([window_size]),'timestamps':np.zeros([window_size])}

    zero_time = time.time()
    while True:
        img = billy.get_frame()
        time_current = time.time() - zero_time

        # Convert from BGR to HSV
        hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.CvtColor(img, hsv, cv.CV_BGR2HSV)

        # Threshold the img in hsv space for green
        img_thresh = cv.CreateImage(cv.GetSize(img), 8, 1)
        cv2.cv.InRangeS(hsv, cv.Scalar(180*145/360, 100, 84), cv.Scalar(180*165/360, 220, 255), img_thresh)

        # Find the centroid of the image
        x,y = find_centroid(img_thresh, billy.cam_width, billy.cam_height)
    
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

        cv.ShowImage("threshholded", img_thresh  )
        cv.ShowImage("camera", img  )   
        if cv.WaitKey(10) == 27:
            break
    cv.DestroyAllWindows()