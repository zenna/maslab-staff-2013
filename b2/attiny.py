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
   def Sense(self):
      byte2 = 0
      byte3 = 0
      byte4 = 0
      self.ser.flushInput()
      self.ser.flushOutput()
      #print(ser.read())
      self.ser.write('s')
      while 1:
         byte1 = byte2
         byte2 = byte3
         byte3 = byte4
         byte4 = ord(ser.read())-ord('0')
         if ((byte1 == 1) & (byte2 == 2) & (byte3 == 3) & (byte4 == 4)):
            break
      a = ord(self.ser.read())
      b = ord(self.ser.read())
      sense0 = 256*b+a
      a = ord(self.ser.read())
      b = ord(self.ser.read())
      sense1 = 256*b+a
      return (sense0, sense1)
   def Tilt(self):
      byte2 = 0
      byte3 = 0
      byte4 = 0
      self.ser.flushInput()
      self.ser.flushOutput()
      #print(ser.read())
      self.ser.write('t')
      while 1:
         byte1 = byte2
         byte2 = byte3
         byte3 = byte4
         byte4 = ord(ser.read())-ord('0')
         if ((byte1 == 1) & (byte2 == 2) & (byte3 == 3) & (byte4 == 4)):
            break
      a = ord(self.ser.read())
      b = ord(self.ser.read())
      sense0 = 256*b+attiny
      a = ord(self.ser.read())
      b = ord(self.ser.read())
      sense1 = 256*b+a
      return (sense0)

class Motor:
   def __init__(self, attiny, fwd_address, bkwd_address):
      self.delay = .002
      self.n_retries = 1
      self.attiny = attiny
      self.fwd_address = fwd_address
      self.bkwd_address = bkwd_address

   # Speed is -255 to 255
   def setSpeed(self, speed):
      # Clamp to [-126, 126]
      if speed < -255:
          speed = -255
      elif speed > 255:
          speed = 255
      
      if speed > 0:
         direction_char = self.fwd_address
      else:
         direction_char = self.bkwd_address

      for i in range(self.n_retries):
         self.attiny.ser.write(direction_char)
         self.attiny.ser.write(chr(abs(speed)))
         time.sleep(self.delay)