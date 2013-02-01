#!/usr/bin/pytshon
# This is a standalone program. Pass an image name as a first parameter of the program.

import sys
from math import sin, cos, sqrt, pi
import cv2
import cv2.cv as cv
import urllib2
import numpy as np

# toggle between CV_HOUGH_STANDARD and CV_HOUGH_PROBILISTIC
USE_STANDARD = True


cv.NamedWindow("camera", 1)

idc_red_range = (cv.Scalar(106,170,145), cv.Scalar(114,185,180))

if __name__ == "__main__":
    filename = sys.argv[1]
    img = cv.LoadImage(filename, cv.CV_LOAD_IMAGE_COLOR)
    hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
    img_thresh = cv.CreateImage(cv.GetSize(img), 8, 1)
    cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
    cv2.cv.InRangeS(hsv, idc_red_range[0], idc_red_range[1], img_thresh)

    while True:
        cv.ShowImage("camera", img_thresh  )   
        if cv.WaitKey(10) == 27:
            break

    cv.DestroyAllWindows()
