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

OnBoard_Button = 5

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

def number_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Light Sensor
class WeLightSensor:
  def __init__(self, port):
    self.port = port  # port:PORT_1~PORT_3

  def getValue(self):
    if self.port == PORT_3:
      self.port = 20
    cmd='M3 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# Sound Sensor
class WeSoundSensor:
  def __init__(self, port):
    self.port = port  # port:PORT_1~PORT_3

  def getValue(self):
    if self.port == PORT_3:
      self.port = 20
    cmd='M3 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# Button On Board
class WeButton:
  def __init__(self, port):
    self.port = port  # port:OnBoard_Button

  def getValue(self):
    cmd='M1 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# DC Motor
class WeDCMotor:
  def __init__(self, port):
    self.port = port  # port:M*
    self.dc_slot = [[None,None],[PORT_1,1], [PORT_1,2], [PORT_2,1], [PORT_2,2], [PORT_3,1], [PORT_3,2]]

  def run(self,speed):  # speed: -255~255
    speed = max(-255, min(255, speed))
    if speed >= 0 :
      speed = (int)(speed/2.55)
    else:
      speed = (int)(100-speed/2.55)

    cmd='M11 '+str(self.dc_slot[self.port][0])+' 2 2 '+str(self.dc_slot[self.port][1])+' '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Encoder Motor
class WeEncoderMotor:
  """docstring for WeEncoderMotor"""
  def __init__(self, port):
    self.port = port  # port:PORT_1~PORT_3

  def run(self, speed):  # speed: -255~255
    cmd='M31 '+str(self.port)+' '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def runSpeed(self, speed):  # speed: -255~255
    cmd='M32 '+str(self.port)+' '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def move(self, speed, position):  # speed: -255~255
    cmd='M33 '+str(self.port)+' '+str(speed)+' '+str(position)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def moveTo(self, speed, position):  # speed: -255~255
    cmd='M34 '+str(self.port)+' '+str(speed)+' '+str(position)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def setPositionOrigin(self):
    cmd='M35 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
  
  def getCurrentPosition(self):
    cmd='M36 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

  def stop(self):
    cmd='M37 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Stepper Motor
class WeStepperMotor:
  """docstring for WeStepperMotor"""
  def __init__(self, port):
    self.port = port  # port:PORT_1~PORT_3

  def run(self):
    cmd='M41 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def stop(self):
    cmd='M42 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def move(self, position):
    cmd='M43 '+str(self.port)+' '+str(position)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def moveTo(self, position):
    cmd='M44 '+str(self.port)+' '+str(position)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def setPositionOrigin(self):
    cmd='M45 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def setSpeed(self, speed):  # speed: 0~254
    cmd='M46 '+str(self.port)+' '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def setMicroStep(self, value):  # value: 1,2,4,8,16,32
    cmd='M47 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# 130 DC Motor Module
class We130DCMotor:
  def __init__(self, port):
    self.port = port     # port:PORT_*

  def run(self,speed):  # speed: -255~255
    speed = max(-255, min(255, speed))
    if speed >= 0 :
      speed = (int)(speed/2.55)
    else:
      speed = (int)(100-speed/2.55)

    cmd='M11 '+str(self.port)+' 2 1 '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Servo
class WeServo:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def write(self, angle):   # angle: 0~180
    cmd='M5 '+str(self.port)+' '+str(angle)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Relay Module
class WeRelay:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def setNC(self, value):  # value: 0, 1
    cmd='M11 '+str(self.port)+' 2 1 '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Atomizer Module
class WeAtomizer:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def setRun(self, value):  # value: 0, 1
    cmd = ''
    if value == 0:
      cmd='M11 '+str(self.port)+' 3 0\r\n'
    elif value == 1:
      cmd='M11 '+str(self.port)+' 2 0\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Vibration Motor
class WeVibrationMotor:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def run(self, speed):  # speed: 0~255
    cmd='M11 '+str(self.port)+' 3 1 '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Joystick Module
class WeJoystick:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):  # index: 0->X, 1->Y
    cmd='M13 '+str(self.port)+' 2 3\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        if index == 0:
          return (255-value[0])
        elif index == 1:
          return value[1]

# 4 LED Button Module
class We4LEDButton:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return value[0]

# Potentiometer Module
class WePotentiometer:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == 3:
        return value[0]

# RGB LED-5 Module
class WeRGB5Module:
  def __init__(self, port):
    self.port = port  # port:PORT_*
    self.RGB_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

  def showRGB(self,index,color):  # index: 0(All),1,2,3,4,5
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(aa[0])
    green=(aa[1])
    blue=(aa[2])
    cmd='M11 '+str(self.port)+' 2 15'
    if index == 0:
      for i in range(0,5):
        index = i * 3
        self.RGB_data[index] = green
        self.RGB_data[index + 1] = red
        self.RGB_data[index + 2] = blue
    elif(index <= 5):
      index = (index - 1) * 3
      self.RGB_data[index] = green
      self.RGB_data[index + 1] = red
      self.RGB_data[index + 2] = blue

    for i in range(0,15):
      cmd = cmd + ' ' + str(self.RGB_data[i])
    cmd = cmd + '\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# RGB Strip
class WeRGBStrip:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def showRGB(self,index,color):  # index: 0(All),1,2,3,4,5,...
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(aa[0])
    green=(aa[1])
    blue=(aa[2])
    cmd='M6 '+str(self.port)+' '+str(index)+' '+str(red)+' '+str(green)+' '+str(blue)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Single LED Module
class WeSingleLED:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def setLight(self, value):  # value: 0, 1
    cmd='M2 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# 4-Digital LED Module
class We7SegmentDisplay:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def showNumber(self, value):  # value: -999~9999
    cmd='M71 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

#  LED Panel Module-Matrix 7*21
class WeLEDPanel_7_21: 
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def showNumber(self, value):  # value: -999~9999
    cmd='M24 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
  
  def showString(self, x, y, string):
    cmd='M26 '+str(self.port)+' '+str(x)+' '+str(y)+' '+string+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def showBitmap(self, x, y, bitmap):
    cmd='M27 '+str(self.port)+' '+str(x)+' '+str(y)
    for i in range(0,21):
      cmd = cmd +' '+str(bitmap[i])
    cmd = cmd + '\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def turnOnDot(self, x, y):
    cmd='M21 '+str(self.port)+' '+str(x)+' '+str(y)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def turnOffDot(self, x, y):
    cmd='M22 '+str(self.port)+' '+str(x)+' '+str(y)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def clearScreen(self):
    cmd='M23 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

# Temperature and Humidity Sensor
class WeHumiture:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):  # index: 0->temperature, 1->humidity
    cmd='M13 '+str(self.port)+' 2 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        if index == 1:
          return value[0]
        elif index == 0:
          return value[1]

# Gas Sensor
class WeGasSensor:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return value[0]

# RGB Ultrasonic Sensor
class WeUltrasonicSensor:
  def __init__(self, port):
    self.port = port  # port:PORT_*
    self.RGB_data=[0,0,0,0,0,0]

  def distanceCM(self):
    cmd='M13 '+str(self.port)+' 2 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        distance = (value[1]<<8|value[0]) / 17.57
        if distance > 500:
          return 500
        else:
          return round(distance,2)

  def showRGB(self,index,color):   # index: 1->right, 2->left, 3->all
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(aa[0])
    green=(aa[1])
    blue=(aa[2])
    cmd='M11 '+str(self.port)+' 3 6'
    if index & 1 != 0:
      self.RGB_data[0]=red
      self.RGB_data[1]=green
      self.RGB_data[2]=blue
    if index & 2 != 0:
      self.RGB_data[3]=red
      self.RGB_data[4]=green
      self.RGB_data[5]=blue
    if index & 3 != 0:
      for i in range(0,6):
        cmd = cmd + ' ' + str(self.RGB_data[i])
      cmd = cmd + '\r\n'
      weSerial.write(bytearray(cmd.encode('utf-8')))
      time.sleep(0.05)

# Single Line Follower Sensor
class WeSingleLineFollower:
  def __init__(self, port):
    self.port = port  # port:PORT_1~PORT_3

  def getValue(self):
    if self.port == PORT_3:
      self.port = 20
    cmd='M3 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return int(1023-eval(value))

# Line Follower Sensor
class WeLineFollower:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):   # index: 1->S1, 2->S2
    cmd='M13 '+str(self.port)+' 2 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        if index == 1:
          return int(number_map(value[0],0,255,1023,0))
        elif index == 2:
          return int(number_map(value[1],0,255,1023,0))

# DS18B20
class WeDS18B20:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self):
    value=''
    cmd='M8 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# PIR Sensor
class WePIRSensor:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return value[0]

# Single Touch Sensor
class WeTouchSensor:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return value[0]

# Color Sensor
class WeColorSensor:
  """docstring for WeColorSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def setLight(self, isOn):
    cmd='M11 '+str(self.port)+' 3 1 '+str(isOn)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def whitebalance(self):
    cmd='M11 '+str(self.port)+' 4 0\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def getValue(self, index):   # index: 1->red, 2->green, 3->blue, 4->light 
    cmd='M13 '+str(self.port)+' 2 8\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        if index == 1:
          return int(value[1]<<8|value[0])
        elif index == 2:
          return int(value[3]<<8|value[2])
        elif index == 3:
          return int(value[5]<<8|value[4])
        elif index == 4:
          return int(value[7]<<8|value[6])

# Flame Sensor
class WeFlameSensor:
  """docstring for WeFlameSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):   # index: 1->S1, 2->S2, 3->S3
    cmd='M13 '+str(self.port)+' 2 3\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        if index == 1:
          return int(value[0])
        elif index == 2:
          return int(value[1])
        elif index == 3:
          return int(value[2])

# Funny Touch
class WeFunnyTouchSensor:
  """docstring for WeFunnyTouchSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0])

# Gesture Touch
class WeGestureSensor:
  """docstring for WeGestureSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0])

# PM2.5 Sensor
class WePM25Sensor:
  """docstring for WePM25Sensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def setFanLaser(self, isOn):
    cmd='M11 '+str(self.port)+' 2 1 '+str(isOn)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.01)

  def readPm1_0Concentration(self):
    cmd='M13 '+str(self.port)+' 3 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def readPm2_5Concentration(self):
    cmd='M13 '+str(self.port)+' 4 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def readPm10Concentration(self):
    cmd='M13 '+str(self.port)+' 5 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def read0_3NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 6 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def read0_5NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 7 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def read1_0NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 8 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def read2_5NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 9 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def read5_0NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 10 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])
  
  def read10NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 11 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

# Tilt Switch
class WeTiltSwitch:
  """docstring for WeTiltSwitch"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return value[0]

# UV Sensor
class WeUVSensor:
  """docstring for WeUVSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return value[0]
  
  def getIndex(self):
    cmd='M13 '+str(self.port)+' 3 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return value[0]

# Water Sensor
class WeWaterSensor:
  """docstring for WeWaterSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return value[0]

# Barometer Sensor
class WeBarometerSensor:
  """docstring for WeBarometerSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def getPressure(self):
    cmd='M13 '+str(self.port)+' 3 4\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return round((value[0]|value[1]<<8|value[2]<<16|value[3]|24)/100,2)
# Gyro Sensor
class WeGyroSensor:
  """docstring for GyroSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
 
  def getValue(self, index):   # index: 0->AngleX, 1->AngleY, 2->AngleZ, 3->AccelerationX, 4->AccelerationY, 5->AccelerationZ
    cmd='M61 '+str(self.port)+' '+str(index)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# Compass Sensor
class WeCompassSensor:
  """docstring for WeCompassSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def getValue(self, index):   # index: 0->X, 1->Y, 2->Z
    cmd='M61 '+str(self.port)+' '+str(index)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

# Adapter Module V2.0
class WeAdapter:
  """docstring for WeAdapter"""
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def servo_write(self,slot,angle):  # slot:1~4  angle:0~180
    cmd='M81 '+str(self.port)+' '+str(slot)+' '+str(angle)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def rgb_show(self,slot,index,color):  # slot:1~4  index:0(All),1,2,3,...  color:#FFFFFF
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(aa[0])
    green=(aa[1])
    blue=(aa[2])
    cmd='M82 '+str(self.port)+' '+str(slot)+' '+str(index)+' '+str(red)+' '+str(green)+' '+str(blue)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def ds18b20_read(self,slot):
    cmd='M83 '+str(self.port)+' '+str(slot)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return round(eval(value),2)
  
  def digital_write(self,slot,value):  # slot:1~4  value:0/1
    cmd='M84 '+str(self.port)+' '+str(slot)+' '+str(vaule)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def digital_read(self,slot):
    cmd='M85 '+str(self.port)+' '+str(slot)+' 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

  def analog_read(self,slot):
    cmd='M86 '+str(self.port)+' '+str(slot)+' 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)