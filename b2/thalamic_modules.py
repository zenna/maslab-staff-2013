import cv2
import cv2.cv as cv


idc_hl = int(62)
idc_sl = int(100)
idc_vl = int(50)

idc_hh = int(82)
idc_sh = int(200)
idc_vh = int(200)

idc_green_range = (cv.Scalar(idc_hl,idc_sl,idc_vl), cv.Scalar(idc_hh,idc_sh,idc_vh))

ridc_hl = int(172)
ridc_sl = int(180)
ridc_vl = int(150)

ridc_hh = int(7)
ridc_sh = int(220)
ridc_vh = int(254)

idc_red_range = (cv.Scalar(ridc_hl,ridc_sl,ridc_vl), cv.Scalar(ridc_hh,ridc_sh,ridc_vh))

yidc_hl = int(20)
yidc_sl = int(133)
yidc_vl = int(121)

yidc_hh = int(27)
yidc_sh = int(193)
yidc_vh = int(243)

idc_yellow_range = (cv.Scalar(yidc_hl,yidc_sl,yidc_vl), cv.Scalar(yidc_hh,yidc_sh,yidc_vh))

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

def threshold_red_balls(img):
	# Threshold the img in hsv space for green
	img_thresh = cv.CreateImage(cv.GetSize(img), 8, 1)
	cv2.cv.InRangeS(img, idc_red_range[0], idc_red_range[1], img_thresh)
	return img_thresh