#########################################
# Adafruit16CServoDriver.py
# description: servo control
# categories: servo control
# more info @: http://myrobotlab.org/service/Adafruit16CServoDriver
#########################################

# This example shows how to use the Adafruit16CServoDriver
# It can be used with Arduino, RasPi or Esp8266_01
# From version 1.0.2316 use attach instead of setController
#
# config
port = "/dev/ttyACM0"
# Code to be able to use this script with virtalArduino
if ('virtual' in globals() and virtual):
    virtualArduino = Runtime.start("virtualArduino", "VirtualArduino")
    virtualArduino.connect(port)
# Start the Adafruit16CServodriver that can be used for all PCA9685 devices
adaFruit16c = Runtime.start("AdaFruit16C","Adafruit16CServoDriver")
#
# This part of the script is for the Arduino
# Comment it out the three lines below if you don't use the Arduino
# Change COM3 to the port where your Arduino is connected
arduino = Runtime.start("arduino","Arduino")
arduino.connect(port)
adaFruit16c.attach("arduino","0","0x40")
#
# This part of the script is if you use the GPOI pins of the Raspberry PI
# Uncomment the two lines below if you use the RasPi
# raspi = Runtime.createAndStart("raspi","RasPi")
# adaFruit16c.attach("raspi","1","0x40")
#
# This part of the script is if you use the Esp8266_01 service
# Uncomment it the two lines below if you duse the Esp8266_01
# esp = Runtime.start("esp","Esp8266_01")
# adaFruit16c.attach("esp","1","0x40")
#
# This part is common for both devices and creates two servo instances
# on port 3 and 8 on the Adafruit16CServoDriver
# Change the names of the servos and the pin numbers to your usage
thumb = Runtime.start("Thumb", "Servo")
index = Runtime.start("Index", "Servo")
majeure = Runtime.start("Majeure", "Servo")
#ringFinger = Runtime.start("Auriculaire", "Servo")
ringFinger = Runtime.start("RingFinger", "Servo")
pinky = Runtime.start("Pinky", "Servo")
wrist = Runtime.start("Wrist", "Servo")

#bicep = Runtime.start("Bicep", "Servo") 
shoulder = Runtime.start("Shoulder", "Servo") 
rotate = Runtime.start("Rotate", "Servo") 
omoplate = Runtime.start("Omoplate", "Servo") 
# attach it to the pwm board - pin 3 & 8
""" 
thumb=180
index=180
majeure=180
ringFinger=180
pinky=180
wrist=180
"""
thumb.attach(adaFruit16c,0)
index.attach(adaFruit16c,4)
majeure.attach(adaFruit16c,3)
pinky.attach(adaFruit16c,1)
ringFinger.attach(adaFruit16c,2)
wrist.attach(adaFruit16c,6)

#bicep.attach(adaFruit16c,0)
shoulder.attach(adaFruit16c,8)
rotate.attach(adaFruit16c,9)
omoplate.attach(adaFruit16c,7)
# When this script has been executed you should be able to
# move the servos using the GUI or using python