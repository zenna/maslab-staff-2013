import random
import sys
sys.path.append("../..")
import time

import arduino

ard = arduino.Arduino()
m0 = arduino.Motor(ard, 0, 42, 9)
m1 = arduino.Motor(ard, 0, 48, 8)
a0 = arduino.AnalogInput(ard, 0)  # Create an analog sensor on pin A0

ard.run()  # Start the Arduino communication thread

def rotate_180(m0, m1):
    m0.setSpeed(90)
    m1.setSpeed(-90)
    time.sleep(random.random() * 3)
    m0.setSpeed(0)
    m1.setSpeed(0)

THRESHOLD = 200

while True:
    m0.setSpeed(-60)
    m1.setSpeed(-60)
    ir_val = a0.getValue() # Note -- the higher value, the *closer* the dist
    if ir_val >= THRESHOLD:
        rotate_180(m0,m1)
