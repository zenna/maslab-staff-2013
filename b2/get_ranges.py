#!/usr/bin/python
# This is a standalone program. Pass an image name as a first parameter of the program.

import sys
from math import sin, cos, sqrt, pi
import cv2.cv as cv
import urllib2
import numpy as np

# toggle between CV_HOUGH_STANDARD and CV_HOUGH_PROBILISTIC
USE_STANDARD = True

cv.NamedWindow("camera", 1)


if __name__ == "__main__":
    filename = sys.argv[1]
    img = cv.LoadImage(filename, cv.CV_LOAD_IMAGE_COLOR)
    hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
    cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
    hsv_np = np.asarray(hsv[:,:])
    print hsv_np.size

    hs = []
    vs = []
    ss = []

    for j in range(hsv.width):
        for i in range(hsv.height):
            hs.append(hsv_np[i,j][0])
            ss.append(hsv_np[i,j][1])
            vs.append(hsv_np[i,j][2])

    # Histogram
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.mlab as mlab
    import pylab as P


    mu, sigma = 100, 15
    x = hs

    fig = P.figure()

    # the histogram of the data
    n, bins, patches = P.hist(x, 30, normed=1, facecolor='green', alpha=0.75)

    P.show()

    x = ss

    fig = P.figure()

    # the histogram of the data
    n, bins, patches = P.hist(x, 30, normed=1, facecolor='green', alpha=0.75)

    P.show()

    x = vs

    fig = P.figure()

    # the histogram of the data
    n, bins, patches = P.hist(x, 30, normed=1, facecolor='green', alpha=0.75)

    P.show()




    cv.DestroyAllWindows()
