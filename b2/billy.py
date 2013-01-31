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
        self.disable_motors()

        #initialisation for pid
        baseline_speed = 0
        self.motor_left_speed = baseline_speed
        self.motor_right_speed = baseline_speed

    def disable_motors(self):
        class FakeMotor():
            def __init__(self, name):
                self.name = name

            def setSpeed(self, speed):
                print "Turning", self.name, speed
        self.motor_left = FakeMotor("left")
        self.motor_right = FakeMotor("right")
        self.roller = FakeMotor("roller")


    def init_arduino(self):
        #setup arduino
        self.ard = arduino.Arduino()
        self.motor_left = arduino.Motor(self.ard, 0, 42, 9, False)
        self.motor_right = arduino.Motor(self.ard, 0, 48, 8, True)
        self.spool = arduino.Motor(self.ard, 0, 30, 11, False)
        self.roller = arduino.Motor(self.ard, 0, 36, 10, False)
        self.latch = arduino.Servo(self.ard, 13)  # Create a Servo object
        self.latch.setAngle(90)
        # Create an analog sensor on pin A0
        self.ir_right = arduino.AnalogInput(self.ard, 0)
        self.ir_centre = arduino.AnalogInput(self.ard, 1)
        self.ir_left = arduino.AnalogInput(self.ard, 2)

        # Switches
        self.color_switch = arduino.DigitalInput(self.ard,31)
        self.reset_switch = arduino.DigitalInput(self.ard,33)
        
        #IMU
        self.imu = arduino.IMU(self.ard)

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
        self.capture = cv.CaptureFromCAM(camera_id)
        self.cam_initialised = True

    def clamp(self, speed, top_speed):
        if speed < -top_speed:
            speed = -top_speed
        elif speed > top_speed:
            speed = top_speed

        return speed

    def single_value_move(self, adjustment):
        print "moving", adjustment
        self.motor_left_speed = self.motor_left_speed + adjustment
        self.motor_right_speed = self.motor_right_speed - adjustment    

        self.motor_left_speed = self.clamp(self.motor_left_speed,30)
        self.motor_right_speed = self.clamp(self.motor_right_speed,30)

        self.motor_left.setSpeed(self.motor_left_speed)
        self.motor_right.setSpeed(self.motor_right_speed)

    def init_windows(self):
        cv.NamedWindow("camera", 1)
        cv.NamedWindow("threshholded", 1)

    # Return infra-red value
    def get_ir(self):
        return self.ir_left.getValue(), self.ir_centre.getValue(), self.ir_right.getValue()

    # Return camera frame
    def get_frame(self):
        if self.cam_initialised == False:
            self.init_camera()
        return cv.QueryFrame(self.capture)

    def in_red_mode(self):
        return self.color_switch.getValue()

    def do_reset(self):
        return self.reset_switch.getValue()

    def get_imu(self):
        return self.imu.getRawValues()

    def show_frame(self):
        cv.ShowImage("camera", self.get_frame())

if __name__ == "__main__":
    cv.WaitKey(10)

    billy = Billy()
    billy.init_camera(1)
    # while True:
    billy.show_frame()

    # cv.DestroyAllWindows()    
