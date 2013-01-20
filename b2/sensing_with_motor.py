#!/usr/bin/python

import cv2
import cv2.cv as cv
import time
import numpy
import pdb

import random
import sys
sys.path.append("..")
import time
import arduino
import attiny

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
        self.att = attiny.ATtiny(port)
        self.motor_right = attiny.Motor(self.att, "n", "m")
        self.motor_left = attiny.Motor(self.att, "p", "o")

    def init_camera(self, camera_id):
        cam_width = self.cam_width = 640
        cam_height = self.cam_height = 480
        indices_x = numpy.tile(range(cam_width),[cam_height,1])
        indices_y = numpy.tile(range(cam_width),[cam_width,1]).transpose()
        indices_y = indices_y[0:cam_height,0:cam_width]
        cv.NamedWindow("camera", camera_id)
        self.capture = cv.CaptureFromCAM(camera_id)
        self.cam_initialised = True

    def get_frame(self):
        if self.cam_initialised == False:
            self.init_camera()
        return cv.QueryFrame(self.capture)

    # Calculate the centroid of ????????
def find_centroid(img_c, cam_width, cam_height):
    img = numpy.asarray(img_c[0:cam_height,0:cam_width]) / 255.0
    total_weight = numpy.sum(img)
    x = numpy.sum(numpy.sum(img * indices_x,0))
    y = numpy.sum(numpy.sum(img * indices_y,0))
    if total_weight != 0:
        x /= total_weight
        y /= total_weight
    return y,x

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

if __name__ == "__main__":

    billy = Billy()
    billy.init_attiny("/dev/serial/by-id/usb-FTDI_TTL232R_FTFBGOT5-if00-port0")
    billy.init_camera(1)

    indices_x = numpy.tile(range(billy.cam_width),[billy.cam_height,1])
    indices_y = numpy.tile(range(billy.cam_width),[billy.cam_width,1]).transpose()
    indices_y = indices_y[0:billy.cam_height,0:billy.cam_width]

    while True:
        img = billy.get_frame()

        # Convert to HSV
        hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
        hue = cv.CreateImage(cv.GetSize(img), 8, 1)
        cv.Split(hsv, hue, None, None, None)
        img_thresh = cv.CreateImage(cv.GetSize(img), 8, 1)

        cv2.cv.InRangeS(hsv, cv.Scalar(180*145/360, 160, 84), cv.Scalar(180*165/360, 220, 255), img_thresh)

        x,y = find_centroid(img_thresh, billy.cam_width, billy.cam_height)
        
        print "CENTROID", x,y
        draw_crosshairs(x,y, img_thresh)
        

        if y > 440:
            billy.motor_right.setSpeed(100)
            billy.motor_left.setSpeed(-100)
            time.sleep(0.2)
            billy.motor_left.setSpeed(0)
            billy.motor_right.setSpeed(0)
            time.sleep(0.2)
        elif y < 340:
            billy.motor_right.setSpeed(-100)
            billy.motor_left.setSpeed(100)
            time.sleep(0.2)
            billy.motor_left.setSpeed(0)
            billy.motor_right.setSpeed(0)
            time.sleep(0.2)
        else:
            billy.motor_right.setSpeed(180)
            billy.motor_left.setSpeed(180)

        cv.ShowImage("camera", img_thresh  )
        if cv.WaitKey(10) == 27:
            break
    cv.DestroyAllWindows()
