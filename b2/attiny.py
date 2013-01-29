import sys,time,serial

# Class that handles sensors and motors for billy
class ATtiny:
   def __init__(self, port):
      self.speed = 9600
      # open serial port
      self.ser = serial.Serial(port, self.speed)
      self.ser.setDTR()
      self.timeout = .1

      # flush buffers
      self.ser.flushInput()
      self.ser.flushOutput()

class Motor:

   # Attiny firmware works by first broadcasting address character
   # Each motor chip has assigned fwd and bkwd address character
   def __init__(self, attiny, fwd_address, bkwd_address, polarity):
      self.delay = .002
      self.attiny = attiny
      self.fwd_address = fwd_address
      self.bkwd_address = bkwd_address
      self.polarity = polarity

   # Sets motor speed between -255 to 255
   def setSpeed(self, speed):
      if polarity == False:
         speed = -speed

      # Clamp to [-126, 126]
      if speed < -255:
          speed = -180
      elif speed > 255:
          speed = 180
      
      if speed > 0:
         direction_char = self.fwd_address
      else:
         direction_char = self.bkwd_address

      self.attiny.ser.write(direction_char)
      self.attiny.ser.write(chr(abs(speed)))
      time.sleep(self.delay)