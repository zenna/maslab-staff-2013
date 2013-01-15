#!/usr/bin/python

import cv2.cv as cv
import cv2
import time
import numpy
import ipdb

# Calculate the centroid of ????????
def find_centroid(img_c):
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

cam_width = 640
cam_height = 480

indices_x = numpy.tile(range(cam_width),[cam_height,1])
indices_y = numpy.tile(range(cam_width),[cam_width,1]).transpose()
indices_y = indices_y[0:cam_height,0:cam_width]
cv.NamedWindow("camera", 1)
capture = cv.CaptureFromCAM(0)


while True:
    img = cv.QueryFrame(capture)
    n = numpy.asarray(img[0:cam_height,0:cam_width]) / 255.0
    r = n[:,:,2]
    b = n[:,:,0]
    g = n[:,:,1]

    # Convert to HSV
    hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
    cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
    hue = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.Split(hsv, hue, None, None, None)
    img_thresh = cv.CreateImage(cv.GetSize(img), 8, 1)

    # n = numpy.zeros([cam_height,cam_width])
    # n[0,0]  = 1.0
    # n[3,639]  = 1.0
    # n[100,639]  = 1.0

    # c is the redness index
    c = r - (g + b) / 2
    c = (c + 1)/2
    c = (hue > 100)

    cv2.cv.InRangeS(hsv, cv.Scalar(70, 100, 0), cv.Scalar(95, 160, 255), img_thresh)
    print "MAX", numpy.max(c)
    print "MIN", numpy.min(c)

    n[:,:,1] = n[:,:,2] = n[:,:,0] = c
    x,y = find_centroid(img_thresh)
    
    print "CENTROID", x,y
    # c_img = cv.fromarray(c)
    draw_crosshairs(x,y, img_thresh)

    # Use NumPy to do some transformat  ions on the image
    cv.ShowImage("camera", img_thresh)
    if cv.WaitKey(10) == 27:
        break
cv.DestroyAllWindows()
