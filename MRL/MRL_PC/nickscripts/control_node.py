import time
import math

leap = Runtime.start("leap","LeapMotion")
leap.addLeapDataListener(python)

http = Runtime.start("http","HttpClient")
# log = Runtime.start("log","Log")

isInitialized      = False
prev_time          = time.time()*1000.0
isHandDisabled     = True
isArmDisabled      = True
isResting          = False
lastArmMovement_ms = 0.0
armRestTimout_ms   = 10.0 * 1000.0

leapFrameProcessDelay = 50.0
fingerMoveThreshold   = 2
leapHandConfidenceThreshold = 0.80

class LeapJoystickThreshold:
  def __init__(self, minimum, maximum):
    self.minimum = minimum
    self.maximum = maximum

leapRightLeftX   = LeapJoystickThreshold(-100, 100)
leapUpDownY      = LeapJoystickThreshold( 120, 210)
leapForwardBackZ = LeapJoystickThreshold( -40,  90)

class HandElement:
  def __init__(self, name, number, previous_sent_angle, angle, angle_mapped, open_max, open_min):
   self.name                = name
   self.number              = number
   self.previous_sent_angle = previous_sent_angle
   self.angle               = angle
   self.angle_mapped        = angle_mapped
   self.open_max            = open_max
   self.open_min            = open_min


thumb      = HandElement("thumb",      0, 0, 0, 0, 100, 60)
index      = HandElement("index",      1, 0, 0, 0, 100,  0)
majeure    = HandElement("majeure",    2, 0, 0, 0, 100,  0)
ringFinger = HandElement("ringFinger", 3, 0, 0, 0, 100,  0)
pinky      = HandElement("pinky",      4, 0, 0, 0, 100,  0)

fingers = [thumb, index, majeure, ringFinger, pinky]

wrist_previous_sent_angle   =   0
wrist_rotate_threshold_high = 160
wrist_rotate_threshold_low  =  10


class ArmElement:
  def __init__(self, name, position, rest, steps, low, high):
    self.name     = name
    self.position = position
    self.rest     = rest
    self.steps    = steps
    self.low      = low
    self.high     = high

# The position, rest, low, and high are placeholders,
# their values are pulled from the Pi upon init.
bicep    = ArmElement("bicep",     5,   5, 4, 0,  90)
omoplate = ArmElement("omoplate", 10,  10, 4, 0, 180)
shoulder = ArmElement("shoulder", 30,  30, 4, 0, 180)
rotate   = ArmElement("rotate",  170, 170, 2, 0, 180)

armElements = [bicep, omoplate, shoulder, rotate]

 
def onLeapData(data):
  global isResting
  global leapFrameProcessDelay
  global prev_time
  global isHandDisabled
  global isArmDisabled
  global lastArmMovement_ms
  global armRestTimout_ms
  global fingers
  global leapHandConfidenceThreshold

  if isInitialized is False:
    return

  current_time = current_time_ms()
  
  if (current_time < prev_time + leapFrameProcessDelay):
    return
  else:
    prev_time = current_time

  for finger in fingers:
    finger.angle        = leap.getJointAngle("right", finger.number)
    finger.angle_mapped = int(map(finger.angle, finger.open_max, finger.open_min, 0.0, 180.0))
  
  angle_sum = 0

  for finger in fingers:
    angle_sum += finger.angle 

  if angle_sum == 0:
    if not isResting:
      print "Hand not found, Resting..."
      isResting = True
    if not isHandDisabled:
      restHand()
    if not isArmDisabled and current_time >= lastArmMovement_ms + armRestTimout_ms:
      print "No arm movement for {}s, resting arm".format(armRestTimout_ms / 1000)
      restArm()
    time.sleep(0.5)
    return
  else:
    isHandDisabled = False
    if (isResting is True):
      isResting    = False
      print "Waking Up..."

  leapHandConfidence = leap.getHandConfidence()
  if leapHandConfidence >= leapHandConfidenceThreshold:
    handleFingers()
  else:
    print "Hand Confidence {}%. Below threshold of {}%, not tracking fingers".format(math.trunc(leapHandConfidence * 100), math.trunc(leapHandConfidenceThreshold * 100))
  handleWristAndRotate()
  handleLeapJoystick()
  return

def handleLeapJoystick():
  global bicep
  global shoulder
  global omoplate
  global fingerMoveThreshold
  global leapForwardBackZ
  global leapRightLeftX

  wristAngle        = leap.getPalmNormal().x
  wristAngle_mapped = int(map(wristAngle,-1, 1, 0, 180))
  palmPosition      = leap.getPalmPosition()
  
  # print "PalmPosition X:{} Y:{} Z:{}".format(palmPosition.x, palmPosition.y, palmPosition.z)
  if (palmPosition.x >= leapRightLeftX.maximum):
    print "Moving Right"
    handleArmPosition(omoplate, "up")
  elif (palmPosition.x <= leapRightLeftX.minimum):
    print "Moving Left"
    handleArmPosition(omoplate, "down")

  if (palmPosition.y >= leapUpDownY.maximum):
    print "Moving Up"
    handleArmPosition(bicep, "up")
  elif (palmPosition.y <= leapUpDownY.minimum):
    print "Moving Down"
    handleArmPosition(bicep, "down")

  if (palmPosition.z <= leapForwardBackZ.minimum):
    print "Moving Forward"
    handleArmPosition(shoulder, "up")
  elif (palmPosition.z >= leapForwardBackZ.maximum):
    print "Moving Backward"
    handleArmPosition(shoulder, "down")

def handleFingers():
  global fingers
  for finger in fingers:
    if abs(finger.angle - finger.previous_sent_angle) >= fingerMoveThreshold:
      http.get("http://roboARM:8888/api/service/inMoovHand." + finger.name + "/moveTo/" + str(finger.angle_mapped))
      finger.previous_sent_angle = finger.angle
  return

def handleWristAndRotate():
  global wrist_previous_sent_angle
  global wrist_rotate_threshold_high
  global wrist_rotate_threshold_low
  global fingerMoveThreshold
  global rotate

  wristAngle        = leap.getPalmNormal().x
  wristAngle_mapped = int(map(wristAngle,-1, 1, 0, 180))
  palmPosition      = leap.getPalmPosition()

  if abs(wristAngle_mapped - wrist_previous_sent_angle) >= fingerMoveThreshold:
    http.get("http://roboARM:8888/api/service/inMoovHand.wrist/moveTo/" + str(wristAngle_mapped))
    wrist_previous_sent_angle = wristAngle_mapped
  #handle rotate
  if (wristAngle_mapped >= wrist_rotate_threshold_high):
    handleArmPosition(rotate, "down")
    print "Rotating Inward"
  elif (wristAngle_mapped <= wrist_rotate_threshold_low):
    handleArmPosition(rotate, "up")
    print "Rotating Outward"
  return

def handleArmPosition(segment, upOrDown):
  global lastArmMovement_ms
  global isArmDisabled
  needsToMove = False
  if (upOrDown == "up"):
    if (segment.position == segment.high):
      pass
    elif (segment.position + segment.steps <= segment.high):
      segment.position += segment.steps
      needsToMove = True
    else:
      segment.position = segment.high
      needsToMove = True
  elif (upOrDown == "down"):
    if (segment.position == segment.low):
      pass
    elif (segment.position - segment.steps >= segment.low):
      segment.position -= segment.steps
      needsToMove = True
    else:
      segment.position = segment.low
      needsToMove = True
  else:
    print "ERROR: Invalid UpOrDown parameter"
    return
  if (needsToMove is True):
    http.get("http://roboARM:8888/api/service/inMoovArm." + segment.name + "/moveTo/" + str(segment.position))
    lastArmMovement_ms = current_time_ms()
    isArmDisabled = False
  print "{}_pos: {}".format(segment.name, segment.position)
  return

def restArm():
  global armElements
  global isArmDisabled
  global isInitialized
  """
  setVelocity(Double bicep, Double rotate, Double shoulder, Double omoplate)
  """
  try:
    http.get("http://roboARM:8888/api/service/inMoovArm/setVelocity/10.0/-1.0/10.0/10.0")
    time.sleep(0.5)
    http.get("http://roboARM:8888/api/service/inMoovArm/rest")
    time.sleep(7.0)
    http.get("http://roboARM:8888/api/service/inMoovArm/disable")
    http.get("http://roboARM:8888/api/service/inMoovArm/setVelocity/-1.0/-1.0/-1.0/-1.0")
    isArmDisabled = True
  except:
    print "ERROR: MRL is not running on the Pi"
  if isInitialized is False:
    print "===============Initializing==============="
    for armElement in armElements:
      armElement.rest = float(http.get("http://roboARM:8888/api/service/inMoovArm." + armElement.name + "/getRest"))
      armElement.low  = float(http.get("http://roboARM:8888/api/service/inMoovArm." + armElement.name + "/getMinInput"))
      armElement.high = float(http.get("http://roboARM:8888/api/service/inMoovArm." + armElement.name + "/getMaxInput"))
      print "Set {}.rest to {}".format(armElement.name, armElement.rest)
      print "Set {}.low to {}".format(armElement.name, armElement.low)
      print "Set {}.high to {}\n".format(armElement.name, armElement.high)
      armElement.position = armElement.rest
    print "===========Initialization Complete==========="
    isInitialized = True
  else:
    for armElement in armElements:
      armElement.position = armElement.rest
  return

def restHand():
  global fingers
  global isHandDisabled

  http.get("http://roboARM:8888/api/service/inMoovHand/rest")
  time.sleep(0.9)
  http.get("http://roboARM:8888/api/service/inMoovHand/disable")
  isHandDisabled = True

  for finger in fingers:
    finger.previous_sent_angle = 0
    finger.angle = 0
    finger.angle_mapped = 0
  return

def current_time_ms():
  return time.time()*1000.0

def map(input, in_min, in_max, out_min, out_max):
  return (input - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

restArm()
restHand()
# try:
#   restArm()
#   restHand()
# except:
#   print "ERROR: Control Node is not connected to Pi Node, check connections and try again"
# leap.startTracking()