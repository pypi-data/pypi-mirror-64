# -*- coding: utf-8 -*-
import serial
import time
from binascii import a2b_hex

weSerial=serial.Serial("/dev/ttyS0",9600,timeout=10)

PORT_A = 16
PORT_B = 17
PORT_C = 18
PORT_D = 19
PORT_1 = 15
PORT_2 = 14
PORT_3 = 6

M1 = 1
M2 = 2
M3 = 3
M4 = 4
M5 = 5
M6 = 6

def colour_rgb(r, g, b):
  r = min(255, max(0, r))
  g = min(255, max(0, g))
  b = min(255, max(0, b))
  return '#%02x%02x%02x' % (r, g, b)

# 130 DC Motor Module
class We130DCMotor:
  def __init__(self, port):
    self.port = port     # port:PORT_*

  def run(self,speed):  # speed: -255~255
    cmd='M204 '+str(self.port)+' '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# DC Motor
class WeDCMotor:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def run(self,speed):  # speed: -255~255
    cmd='M200 '+str(self.port)+' '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Servo
class WeServo:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def write(self, angle):   # angle: 0~180
    cmd='M202 '+str(self.port)+' '+str(angle)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Temperature and Humidity Sensor
class WeHumiture:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):  # index: 0->temperature, 1->humidity
    value=''
    cmd='M122 '+str(self.port)+' '+str(index)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# Gas Sensor
class WeGasSensor:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self):
    value=''
    cmd='M126 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# RGB Ultrasonic Sensor
class WeUltrasonicSensor:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def distanceCM(self):
    distance=""
    cmd='M110 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

  def showRGB(self,index,color):   # index: 1->right, 2->left, 3->all
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(ord(aa[0]))
    green=(ord(aa[1]))
    blue=(ord(aa[2]))
    cmd='M109 '+str(self.port)+' '+str(index)+' '+str(red)+' '+str(green)+' '+str(blue)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# RGB LED-5 Module
class WeRGB5Module:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def showRGB(self,index,color):  # index: 0(All),1,2,3,4,5
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(ord(aa[0]))
    green=(ord(aa[1]))
    blue=(ord(aa[2]))
    cmd='M13 '+str(self.port)+' '+str(index)+' '+str(red)+' '+str(green)+' '+str(blue)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# RGB Strip
class WeRGBStrip:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def showRGB(self,index,color):  # index: 0(All),1,2,3,4,5,...
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(ord(aa[0]))
    green=(ord(aa[1]))
    blue=(ord(aa[2]))
    cmd='M9 '+str(self.port)+' '+str(index)+' '+str(red)+' '+str(green)+' '+str(blue)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Joystick Module
class WeJoystick:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):  # index: 0->X, 1->Y
    value=''
    temp=''
    cmd='M22 '+str(self.port)+' '+str(index)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# Line Follower Sensor
class WeLineFollower:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):   # index: 1->S1, 2->S2
    value=''
    cmd='M111 '+str(self.port)+' '+str(index)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# DS18B20
class DS18B20:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self):
    value=''
    cmd='M12 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# Potentiometer Module
class WePotentiometer:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def getValue(self):
    value=''
    cmd='M126 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# Relay Module
class WeRelay:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def setNC(self, value):  # value: 0, 1
    cmd='M26 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Atomizer Module
class WeAtomizer:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def setRun(self, value):  # value: 0, 1
    cmd='M27 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Single LED Module
class WeSingleLED:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def setLight(self, value):  # value: 0, 1
    cmd='M125 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# 4-Digital LED Module
class We7SegmentDisplay:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def showNumber(self, value):  # value: -999~9999
    cmd='M123 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

#  LED Panel Module-Matrix 7*21
class WeLEDPanel_7_21: 
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def showNumber(self, value):  # value: -999~9999
    cmd='M112 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
  
  def showString(self, x, y, string):
    cmd='M114 '+str(self.port)+' '+str(x)+' '+str(y)+' '+string+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def turnOnDot(self, x, y):
    cmd='M1 '+str(self.port)+' '+str(x)+' '+str(y)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def turnOffDot(self, x, y):
    cmd='M2 '+str(self.port)+' '+str(x)+' '+str(y)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def clearScreen(self):
    cmd='M3 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)