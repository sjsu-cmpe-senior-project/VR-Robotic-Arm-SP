import time
import math

leap = Runtime.start("leap","LeapMotion")
 
leap.addLeapDataListener(python)

http = Runtime.start("http","HttpClient")


prev_time = time.time()*1000.0
isDisabled = True

leapFrameProcessDelay = 50

fingerMoveThreshold = 2

class HandElement:
  def __init__(self, name, number, previous_sent_angle, angle, angle_mapped, open_max, open_min):
   self.name                = name
   self.number              = number
   self.previous_sent_angle = previous_sent_angle
   self.angle               = angle
   self.angle_mapped        = angle_mapped
   self.open_max            = open_max
   self.open_min            = open_min


thumb      = HandElement("thumb",      0, 0, 0, 0, 100, 40)
index      = HandElement("index",      1, 0, 0, 0, 100, 0)
majeure    = HandElement("majeure",    2, 0, 0, 0, 100, 0)
ringFinger = HandElement("ringFinger", 3, 0, 0, 0, 100, 0)
pinky      = HandElement("pinky",      4, 0, 0, 0, 100, 0)

wrist_previous_sent_angle = 0

fingers = [thumb, index, majeure, ringFinger, pinky]

class ArmElement:
  def __init__(self, name, position, steps, low, high):
    self.name = name
    self.position = position
    self.steps = steps
    self.low = low
    self.high = high

bicep    = ArmElement("bicep",    0, 4, 0, 90)
omoplate = ArmElement("omoplate", 0, 4, 0, 180)
shoulder = ArmElement("shoulder", 0, 4, 0, 180)
rotate   = ArmElement("rotate",   0, 4, 0, 180)
 

def current_time_ms():
  return time.time()*1000.0

def map(input, in_min, in_max, out_min, out_max):
  return (input - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def onLeapData(data):
  #print (data.rightHand.index)

  current_time = current_time_ms()
  global leapFrameProcessDelay
  global prev_time
  global isDisabled

  global bicep
  global shoulder
  global omoplate
  global fingers
  global fingerMoveThreshold
  global wrist_previous_sent_angle


  leapFrame = leap.controller.frame()
  leapHand =  leap.controller.frame().hands().rightmost()

  if (current_time < prev_time + leapFrameProcessDelay):
    return
  else:
    prev_time = current_time

  for finger in fingers:
    finger.angle = leap.getJointAngle("right", finger.number)
    # finger.previous_angle = finger.angle_mapped
    finger.angle_mapped = int(map(finger.angle, finger.open_max, finger.open_min, 0.0, 180.0))

  angle_sum = 0

  for finger in fingers:
    angle_sum += finger.angle 

  if angle_sum == 0:
    print "Hand not found, Resting"
    if not isDisabled:
      # http.get("http://roboARM:8888/api/service/inMoovHand/rest")
      time.sleep(0.9)
      # http.get("http://roboARM:8888/api/service/inMoovHand/disable")
      isDisabled = True
    time.sleep(0.5)
    return
  else:
    isDisabled = False
  
  wristAngle = leap.getPalmNormal().x
  wristAngle_mapped = int(map(wristAngle,-1, 1, 0, 180))
  palmPosition = leap.getPalmPosition()
  
  print "PalmPosition X:{} Y:{} Z:{}".format(palmPosition.x, palmPosition.y, palmPosition.z)
  if (palmPosition.x > 100):
    print "Moving Right"
    # handleArmPosition(omoplate, "up")
  elif (palmPosition.x < -100):
    print "Moving Left"
    # handleArmPosition(omoplate, "down")

  if (palmPosition.y > 210):
    print "Moving Up"
    # handleArmPosition(bicep, "up")
  elif (palmPosition.y < 120):
    print "Moving Down"
    # handleArmPosition(bicep, "down")

  if (palmPosition.z < -40):
    print "Moving Forward"
    # handleArmPosition(shoulder, "up")
  elif (palmPosition.z > 90):
    print "Moving Backward"
    # handleArmPosition(shoulder, "down")

  # for finger in fingers:
  #   if abs(finger.angle - finger.previous_sent_angle) >= fingerMoveThreshold:
  #     http.get("http://roboARM:8888/api/service/inMoovHand."+finger.name+"/moveTo/" + str(finger.angle_mapped))
  #     finger.previous_sent_angle = finger.angle
  # if abs(wristAngle_mapped - wrist_previous_sent_angle) >= fingerMoveThreshold:
  #   http.get("http://roboARM:8888/api/service/inMoovHand.wrist/moveTo/" + str(wristAngle_mapped))
  #   wrist_previous_sent_angle = wristAngle_mapped

def handleArmPosition(segment, upOrDown):
  if (upOrDown == "up"):
    needsToMove = False
    if (segment.position == segment.high):
      pass
    elif (segment.position + segment.steps <= segment.high):
      segment.position += segment.steps
      needsToMove = True
    else:
      segment.position = segment.high
      needsToMove = True
    if (needsToMove == True):
      http.get("http://roboARM:8888/api/service/inMoovArm." + segment.name + "/moveTo/" + str(segment.position))
    print "{}_pos: {}".format(segment.name, segment.position)
  elif (upOrDown == "down"):
    needsToMove = False
    if (segment.position == segment.low):
      pass
    elif (segment.position - segment.steps >= segment.low):
      segment.position -= segment.steps
      needsToMove = True
    else:
      segment.position = segment.low
      needsToMove = True
    if (needsToMove == True):
      http.get("http://roboARM:8888/api/service/inMoovArm." + segment.name + "/moveTo/" + str(segment.position))
    print "{}_pos: {}".format(segment.name, segment.position)
  return

leap.startTracking()