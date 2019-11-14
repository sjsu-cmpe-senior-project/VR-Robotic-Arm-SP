#i01 = Runtime.createAndStart("i01", "InMoov")
arm = Runtime.createAndStart("arm", "Adafruit16CServoDriver")
#rightHand = Runtime.createAndStart("rightHand", "Adafruit16CServoDriver")

# port="/dev/ttyACM0"

raspi = Runtime.createAndStart("raspi","RasPi")

# arduino = Runtime.start("arduino","Arduino")
# arduino.connect(port)

arm.setController("raspi","1","0x40")

# bicep = Runtime.createAndStart("Bicep", "Servo")
# bicep.attach(arm,15)
# bicep.setMinMax(0,90)
# bicep.map(0,180,0,90)

omoplate = Runtime.createAndStart("Omoplate", "Servo")
omoplate.attach(arm,7)
# omoplate.setMinMax(10,80)
omoplate.map(0,180,10,80)

shoulder_rotate = Runtime.createAndStart("ShoulderRotate", "Servo")
shoulder_rotate.attach(arm,8)
# shoulder_rotate.setMinMax(0,90)
shoulder_rotate.map(0,180,0,90)

arm_rotate = Runtime.createAndStart("ArmRotate", "Servo")
arm_rotate.attach(arm,9)
# arm_rotate.setMinMax(90,170)
arm_rotate.map(0,180,90,170)

wrist = Runtime.createAndStart("Wrist", "Servo")
wrist.attach(arm,6)
wrist.setMinMax(0,180)

thumb = Runtime.createAndStart("Thumb", "Servo")
thumb.attach(arm,0)
thumb.setMinMax(0,180)
 
index = Runtime.createAndStart("Index", "Servo")
index.attach(arm,4)
index.setMinMax(0,180)
 
majeure = Runtime.createAndStart("Majuere", "Servo")
majeure.attach(arm,3)
majeure.setMinMax(0,180)
 
ring = Runtime.createAndStart("RingFinger", "Servo")
ring.attach(arm,2)
ring.setMinMax(0,180)

pinky = Runtime.createAndStart("Pinky", "Servo")
pinky.attach(arm,1)
pinky.setMinMax(0,180)

remote = Runtime.createAndStart("Pi","RemoteAdapter")

remote.startListening()