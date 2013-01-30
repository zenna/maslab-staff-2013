from billy import *
import cv2
import cv2.cv as cv
import sys

if __name__ == "__main__":
    camera_id = sys.argv[1]
    print camera_id
    billy = Billy()
    billy.init_camera(int(camera_id))
    while True:
    	billy.show_frame()
    	if cv.WaitKey(10) == 27:
    	    break

    cv.DestroyAllWindows()    
