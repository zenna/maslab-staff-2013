import cv2
import cv2.cv as cv


idc_hl = int(67)
idc_sl = int(100)
idc_vl = int(50)

idc_hh = int(82)
idc_sh = int(200)
idc_vh = int(180)

idc_green_range = (cv.Scalar(idc_hl,idc_sl,idc_vl), cv.Scalar(idc_hh,idc_sh,idc_vh))

# Reduce image size
def bgr_to_hsv(img):
	# Convert from BGR to HSV
	hsv = cv.CreateImage(cv.GetSize(img), 8, 3)
	cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
	return hsv

def threshold_green_balls(img):
	# Threshold the img in hsv space for green
	img_thresh = cv.CreateImage(cv.GetSize(img), 8, 1)
	cv2.cv.InRangeS(img, idc_green_range[0], idc_green_range[1], img_thresh)
	return img_thresh
