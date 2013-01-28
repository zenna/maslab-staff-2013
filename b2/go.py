import attiny

att = attiny.ATtiny("/dev/serial/by-id/usb-FTDI_TTL232R_FTFBGOT5-if00-port0")
motor_right = attiny.Motor(att, "n", "m")
motor_left = attiny.Motor(att, "o", "p")
motor_left.setSpeed(0)
motor_right.setSpeed(0)