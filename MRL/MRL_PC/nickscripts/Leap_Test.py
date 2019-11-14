leap = Runtime.start("leap","LeapMotion")
 
leap.addLeapDataListener(python)
 
def onLeapData(data):
  #print (data.rightHand.index)
  angle_thumb = leap.getJointAngle("right", 0)
  angle_index = leap.getJointAngle("right", 1)
  angle_middle = leap.getJointAngle("right", 2)
  angle_ring = leap.getJointAngle("right", 3)
  angle_pinky = leap.getJointAngle("right", 4)
  print "angle_thumb: {}".format(angle_thumb)
  print "angle_index: {}".format(angle_index)
  print "angle_middle: {}".format(angle_middle)
  print "angle_ring: {}".format(angle_ring)
  print "angle_pinky: {}".format(angle_pinky)
 
leap.startTracking()