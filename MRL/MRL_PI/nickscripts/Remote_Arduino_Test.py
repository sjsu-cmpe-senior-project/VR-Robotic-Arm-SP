
#rightHand = Runtime.createAndStart("rightHand", "Adafruit16CServoDriver")

port="/dev/ttyACM0"
i01 = Runtime.create("i01", "InMoov")

#i01.startRightArm(port)
i01.startRightHand(port)


# arduino = Runtime.start("arduino","Arduino")
# arduino.connect(port)

#arm = Runtime.createAndStart("arm", "Inmoo")

remote = Runtime.createAndStart("Pi","RemoteAdapter")



remote.startListening()