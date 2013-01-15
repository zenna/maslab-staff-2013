#!/usr/bin/python

import cv2.cv as cv
import time
import numpy
import pdb

import random
import sys
sys.path.append("..")
import time
import arduino

#setup arduino
ard = arduino.Arduino()
m0 = arduino.Motor(ard, 0, 42, 9)
m1 = arduino.Motor(ard, 0, 48, 8)
a0 = arduino.AnalogInput(ard, 0)  # Create an analog sensor on pin A0

ard.run()  # Start the Arduino communication thread

# Calculate the centroid of ????????
def find_centroid(img):
    total_weight = numpy.sum(img)
    x = numpy.sum(numpy.sum(img * indices_x,0))
    y = numpy.sum(numpy.sum(img * indices_y,1))

    x /= total_weight
    y /= total_weight
    return x,y

def draw_crosshairs(x,y, img):
    import random
    x = int(x)
    y = int(y)
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

indices_x = numpy.tile(range(480),[480,1])
indices_y = indices_x.transpose()

cv.NamedWindow("camera", 1)

capture = cv.CaptureFromCAM(0)

while True:
    img = cv.QueryFrame(capture)
    n = numpy.asarray(img[0:480,0:480]) / 255.0
    r = n[:,:,2]
    b = n[:,:,0]
    g = n[:,:,1]
    #baseline = numpy.mean([b,g],2)
    #c = g - baseline
    # c is the redness index
    c = r - (g + b) / 2
    n[:,:,1] = n[:,:,2] = n[:,:,0] = c
    x,y = find_centroid(c)
    img = cv.fromarray(n)
    draw_crosshairs(x,y, img)
    # print x,y
    
    if x > 280:
        m0.setSpeed(40)
        m1.setSpeed(-40)
    elif x < 220:
        m0.setSpeed(-40)
        m1.setSpeed(40)
    else:
        m0.setSpeed(40)
        m1.setSpeed(40)


    cv.ShowImage("camera", img)
    if cv.WaitKey(10) == 27:
        break
cv.DestroyAllWindows()
