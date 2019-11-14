##################################################
# Inverse Kinematics
# This is an example to build up a robot arm
# using (modified?) DH parameters
# then use the InverseKinematics3D service to
# compute the forward and inverse kinematics for 
# the arm.
##################################################
import math
from time import sleep
from org.myrobotlab.service import InMoovArm
from org.myrobotlab.kinematics import DHRobotArm
from org.myrobotlab.kinematics import DHLink
from org.myrobotlab.kinematics import DHLinkType

# Create a robot arm
arm = DHRobotArm()

link1 = DHLink("omoplate", 0, 40, math.radians(-90), math.radians(-90))
link1.setMin(math.radians(-90))
link1.setMax(math.radians(0))
#/link1.setOffset(90)

link2 = DHLink("shoulder", -80, 0, math.radians(90), math.radians(90))
link2.setMin(math.radians(-90))
link2.setMax(math.radians(90))
#/link2.setOffset(-45)

link3 = DHLink("rotate", 280, 0, math.radians(0), math.radians(90))
link3.setMin(math.radians(-90))
link3.setMax(math.radians(90))
#/link3.setOffset(0)

link4 = DHLink("bicep", 0, 280, math.radians(90), math.radians(0))
link4.setMin(math.radians(90))
link4.setMax(math.radians(180))
#/link4.setOffset(-90)

arm.addLink(link1)
arm.addLink(link2)
arm.addLink(link3)
arm.addLink(link4)


# create the  IK3D service.
ik3d= Runtime.createAndStart("ik3d", "InverseKinematics3D")

# assign our custom DH robot arm to the IK service.
ik3d.setCurrentArm(arm)


# print out the current postion of the arm.
print ik3d.getCurrentArm().getPalmPosition()


# Now, pick a start/end point 
# and begin moving along a stright line as specified by the start/stop point.

# starting point
# x , y , z
x1 = 100
y1 = 100
z1 = 100

# ending point
# x , y , z
x2 = 200
y2 = -400
z2 = 100

# how many steps will we take to get there
numSteps = 100
# delay between steps (in seconds) (this will control the velocity of the end effector.
delay = 0.1 

# lets compute how long the path is.
# this is the change in x,y,z between the two points
# divided up into numSteps, so we know how much to
# move in the x,y,z direction for each step.
dx = 1.0*(x2 - x1)/numSteps
dy = 1.0*(y2 - y1)/numSteps
dz = 1.0*(z2 - z1)/numSteps

# our starting point for the iteratin
# set that to the current x,y,z position 
curX = x1
curY = y1
curZ = z1

# tell the arm to configure to that point
ik3d.moveTo(curX,curY,curZ)

# iterate over the 100 steps
for i in range(0 , 100):
  # Increment our desired current position by dx,dy,dz 
  curX+=dx
  curY+=dy  
  curZ+=dz
# tell the ik engine to move to that new point
  ik3d.moveTo(curX, curY, curZ)    
  # pause for a moment to let the arm arrive at it's destination
  # smaller delay = faster movement.
  sleep(delay)