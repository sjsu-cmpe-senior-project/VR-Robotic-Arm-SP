import time

WebGui = Runtime.create("WebGui","WebGui")
 
WebGui.hide('cli')
sleep(1)
WebGui.show('cli')
sleep(1)
WebGui.set('cli', 400, 400, 999)
 
# if you don't want the browser to 
# autostart to homepage
#
WebGui.autoStartBrowser(False)
WebGui.startService()

controller = Runtime.createAndStart("i2cController", "Adafruit16CServoDriver")

raspi = Runtime.createAndStart("raspi","RasPi")

controller.setController("raspi","1","0x40")

inMoovArm = Runtime.createAndStart("inMoovArm", "InMoovArm")

inMoovArm.bicep.attach(controller, 5)
inMoovArm.bicep.map(0,90,5,85)
inMoovArm.bicep.setRest(5.0)

inMoovArm.omoplate.attach(controller, 7)
inMoovArm.omoplate.map(0,180,10,80)
inMoovArm.omoplate.setRest(10.0)

inMoovArm.shoulder.attach(controller, 8)
inMoovArm.shoulder.map(0,180,0,90)
inMoovArm.shoulder.setRest(30.0)

inMoovArm.rotate.attach(controller, 9)
inMoovArm.rotate.map(0,180,90,170)
inMoovArm.rotate.setRest(180.0)

inMoovArm.disable()

# Create Hand
inMoovHand = Runtime.createAndStart("inMoovHand", "InMoovHand")
inMoovHand.setSide("right")
inMoovHand.setVelocity(-1,-1,-1,-1,-1,-1)
inMoovHand.thumb.attach(controller, 0)
inMoovHand.index.attach(controller, 4)
inMoovHand.majeure.attach(controller, 3)
inMoovHand.pinky.attach(controller, 1)
inMoovHand.ringFinger.attach(controller, 2)
inMoovHand.wrist.attach(controller, 6)
# setRest(double thumb, double index, double majeure, double ringFinger, double pinky, Double wrist)
inMoovHand.setRest(43.0, 5.0, 40.0, 45.0, 40.0, 90.0)
inMoovHand.disable()

# inMoovHand.ok()
# inMoovHand.waitTargetPos()
# reset()

# inMoovHand.rest()
# inMoovHand.waitTargetPos()
# reset()

# inMoovHand.one()
# inMoovHand.waitTargetPos()
# reset()

# inMoovHand.two()
# inMoovHand.waitTargetPos()
# reset()

# inMoovHand.three()
# inMoovHand.waitTargetPos()
# reset()

# inMoovHand.victory()
# inMoovHand.waitTargetPos()
# reset()

# inMoovHand.ok()
# inMoovHand.waitTargetPos()
# reset()

# inMoovHand.thumbsUp()
# inMoovHand.waitTargetPos()
# reset()

# def reset():
#     inMoovHand.rest()
#     inMoovHand.waitTargetPos()


# Create InMoov Instance
# inMoov = Runtime.createAndStart("inMoov", "InMoov")
# inMoov.setRightArm(inMoovArm)
# inMoov.setRightHand(inMoovHand)



# bicep = Runtime.createAndStart("Bicep", "Servo")
# bicep.attach(arm,5)
# # bicep.setMinMax(0,90)
# bicep.map(0,90,5,85)
# bicep.disable()

# omoplate = Runtime.createAndStart("Omoplate", "Servo")
# omoplate.attach(arm,7)
# # omoplate.setMinMax(10,80)
# omoplate.map(0,180,10,80)
# omoplate.disable()

# shoulder_rotate = Runtime.createAndStart("ShoulderRotate", "Servo")
# shoulder_rotate.attach(arm,8)
# # shoulder_rotate.setMinMax(0,90)
# shoulder_rotate.map(0,180,0,90)
# shoulder_rotate.disable()

# arm_rotate = Runtime.createAndStart("ArmRotate", "Servo")
# arm_rotate.attach(arm,9)
# # arm_rotate.setMinMax(90,170)
# arm_rotate.map(0,180,90,170)
# arm_rotate.disable()

# wrist = Runtime.createAndStart("Wrist", "Servo")
# wrist.attach(arm,6)
# wrist.setMinMax(0,180)
# wrist.disable()

# thumb = Runtime.createAndStart("Thumb", "Servo")
# thumb.attach(arm,0)
# thumb.setMinMax(0,180)
# thumb.disable()
 
# index = Runtime.createAndStart("Index", "Servo")
# index.attach(arm,4)
# index.setMinMax(0,180)
# index.disable()
 
# majeure = Runtime.createAndStart("Majeure", "Servo")
# majeure.attach(arm,3)
# majeure.setMinMax(0,180)
# majeure.disable()
 
# ring = Runtime.createAndStart("RingFinger", "Servo")
# ring.attach(arm,2)
# ring.setMinMax(0,180)
# ring.disable()

# pinky = Runtime.createAndStart("Pinky", "Servo")
# pinky.attach(arm,1)
# pinky.setMinMax(0,180)
# pinky.disable()

# # Try to attach to InMoovArm
# inMoovArm = Runtime.createAndStart("InMoovArm", "InMoovArm")
# # # inMoovArm.setController(arm)
# inMoovArm.setBicep(bicep)
# inMoovArm.setOmoplate(omoplate)
# inMoovArm.setRotate(arm_rotate)
# inMoovArm.setShoulder(shoulder_rotate)
# inMoovArm.setSide("right")
# inMoovArm.enable()
# inMoovArm.attach()
# inMoovArm.omoplate.setController(arm)
# inMoovArm.bicep.setController(arm)
# inMoovArm.rotate.setController(arm)
# inMoovArm.shoulder.setController(arm)
# inMoovArm.setVelocity(-1, -1, -1, -1)
# inMoovArm.broadcastState()

# inMoovArm.bicep.attach(arm,5)
# inMoovArm.bicep.enable()
# inMoovArm.bicep.broadcastState()
# inMoovArm.rotate.setController(arm)
# inMoovArm.shoulder.setController(arm)
# inMoovArm.attach()


#remote = Runtime.createAndStart("Pi","RemoteAdapter")

#remote.startListening()

# WebGui = Runtime.create("WebGui","WebGui")
 
# WebGui.hide('cli')
# sleep(1)
# WebGui.show('cli')
# sleep(1)
# WebGui.set('cli', 400, 400, 999)
 
# # if you don't want the browser to 
# # autostart to homepage
# #
# WebGui.autoStartBrowser(False)
 
# set a different port number to listen to
# default is 8888
# WebGui.setPort(7777)
 
# on startup the WebGui will look for a "resources"
# directory (may change in the future)
# static html files can be placed here and accessed through
# the WebGui service
 
# starts the websocket server
# and attempts to autostart browser
#WebGui.startService();
