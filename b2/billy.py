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
        self.motor_right = arduino.Motor(self.ard, 0, 42, 9)
        self.motor_left = arduino.Motor(self.ard, 0, 48, 8)
        self.a0 = arduino.AnalogInput(self.ard, 0)  # Create an analog sensor on pin A0
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

    # Return infra-red value
    def get_ir(self):
        return self.a0.getValue()

    # Return camera frame
    def get_frame(self):
        if self.cam_initialised == False:
            self.init_camera()
        return cv.QueryFrame(self.capture)

    def show_frame(self):
        cv.ShowImage("camera", self.get_frame()) 

    def single_value_move(self, move):
        print "moving", move
        baseline_speed = 130
        self.motor_left.setSpeed(int(baseline_speed+move/2.))
        self.motor_right.setSpeed(int(baseline_speed-move/2.))

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
    return y - 300

def integrate_errors(past_errors):
    integral = scipy.integrate.trapz(past_errors['errors'], past_errors['timestamps'])
    return integral

def find_deriviative(past_errors):
    return (past_errors['errors'][-1] - past_errors['errors'][-2]) / (past_errors['timestamps'][-1] - past_errors['timestamps'][-2])

if __name__ == "__main__":
    cv.WaitKey(10)

    billy = Billy()
    billy.init_camera(1)
    # while True:
    billy.show_frame()

    # cv.DestroyAllWindows()    