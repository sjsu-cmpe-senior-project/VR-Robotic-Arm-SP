# Remote Controlled 3D-Printed Robotic Arm in VR

The goal of the project was to design, develop, and implement a low-cost 3D printed robotic arm that is controlled by a user’s hand gestures based on the video stream displayed into a virtual reality headset. At the beginning of the project, the following objectives were set:

  

1.  3D print all the robotic arm parts through the 3D printing services available in SJSU’s College of Engineering before the end of April 2019.
    
2.  Research, purchase, and gather all the needed hardware materials such as servo motors, virtual reality headset, leap motion sensor, microcontroller, and miscellaneous hardware before the end of May 2019.
    
3.  Assemble the 3D printed robotic arm parts with all the hardware acquired yielding a functional right arm by the end of September 2019.
    
4.  Program microcontroller, and a motion controller software application which reflects the user’s gestures on the arm as well as develop the video streaming interface between from arm’s camera to the virtual reality headset using Unity by the end of October 2019.
    

This robotic arm is ideal for performing precise or hazardous tasks that could be either fatal to their human counterparts or complicated for other types of robotic arms. This device remedies these issues via the use of remote operation.

# Demo Video
[![Demo Video](https://i.ibb.co/4fsybqx/https-drive-google.jpg)](https://drive.google.com/file/d/1X--VK2AbDdoplTd53PcimobloKXxQMyF/view "Demo Video")


## Repo Structure
Almost all of the software resources for this project are located in the `MRL` folder of this repo. They are separated into folder for the Raspberry Pi Node (`MRL_PI`) and PC Node (`MRL_PC`). Additionally, there is a folder called `MRL_SOURCE` that contains the modified source code for compiling the MRL runtime. However, this folder does not need to be addressed unless you are planning on adding additional functionality. 

## Software Requirements 
* Java 8 JRE seems to work the best for this application.
* Linux Environment for PC and PI nodes. (We used [Manjaro](https://manjaro.org/) for the PC and [DietPi](https://dietpi.com/) for the Raspberry Pi 4)
* [mjpg-streamer](https://github.com/jacksonliam/mjpg-streamer)
* [Gizmo VR Player](https://gizmovr.com/)

## Runtime Information

The repo already contains a compiled runtime executable for each node called `myrobotlab.jar`. This is a modified version of [this MRL release](https://github.com/MyRobotLab/myrobotlab/releases/tag/1.0.2693) in which additional functionality was added to properly utilize the [Adafruit I2C PWM servo controller](https://www.adafruit.com/product/815) as well as the [Leap Motion Controller](https://www.leapmotion.com/). 

We have developed this project for use in a Linux environment and these instructions will assume that. However, it would be trivial to port to another OS, mainly the bash scripts would need to be modified.

## Networking Setup
This project utilizes a dedicated WiFi router that is attached to the robot's chest. We used a [TP-Link Archer C7 v2](https://www.tp-link.com/us/support/download/archer-c7/v2/) but any WiFi router should be sufficient. 

Once connected to the router, create a 5G network called `roboARM`. This is crucial for the networking to function properly. Additionally, make sure that the router's local IP is `192.168.1.1` We made our network hidden but this is up to you.

Next, it is very useful to configure static IP addresses for both your PC and PI node. The process for doing this varies by manufacturer but should be found in the LAN settings. Once this is complete, add an entry to the PC Node's `/etc/hosts`file as follows: `192.168.1.101 roboARM`replacing the `192.168.1.101`with the static IP of the PC Node. This does not need to be done on the PI.

## PC Node Setup
Refer to the previous section regarding the networking setup for the PC Node. 

Next, download the `MRL_PC`folder from this repo and open a terminal in this folder.  

Run `java -jar ./myrobotlab.jar --install` This should take some time as it needs to download all of the dependencies that are not included in the repository.  Continue with the `PI Node Setup` section and then return here.
 
Once the PI node is running, connect the Leap Motion controller to the PC. Then run `sudo ./leapd --run` this will start the leap daemon so that the control software can track hand movements. 

Once the leap daemon is running, in a new terminal tab execute `./Start_PC.sh` This script will start all of the necessary components. 

Once the MRL window has appeared, click on the `python` tab to see the output. 

Additionally, you can open a web browser and open `http://roboARM:8080/?action=stream` to view the VR feed from a PC.

## PI Node Setup
For the initial PI Node setup, the PI requires internet access. After the setup phase, it will no longer need to access the internet.

Because the PI is headless you will need to `ssh` into it by running `ssh root@roboARM` on the PC. 

First, download the MRL_PC folder from the repo and make sure the Java 8 JRE is installed and selected. 

Next, open a terminal in the MRL_PI folder and run `java -jar ./myrobotlab.jar --install` to automatically download all of the dependencies (this only needs to be done once). 

Run `dietpi-config` and enable the I2C functionality for the servo controller. Next, connect the I2C servo controller as shown [here](https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/hooking-it-up). 

Then, install `mjpeg-streamer` as shown at [this link](https://github.com/jacksonliam/mjpg-streamer). 

Once these steps are complete, the PI no longer needs to be connected to the internet. 

Run `dietpi-config` and navigate to the networking settings. Here, enable the Ethernet port and disable the onboard WiFi. The PI is connected via Ethernet to the onboard router.

At this point you will lose connection to the PI. On the PC, connect to the roboARM WiFi network and once again ssh into the PI with `ssh root@roboARM`

In the MRL_PI folder, there is a script called `autostart.sh` which will be used to configure the PI upon every boot.  

You need to configure this script to run at boot. In this case we are using DietPi OS. You can run `dietpi-autostart` and select `custom script`. Then, place this file in `/var/lib/dietpi/dietpi-autostart/` and rename to `custom.sh`. 

**NOTE**: you may need to change line 18 of the script to reflect where your `MRL_PI` folder is located. 

Now plug your [webcam](https://www.logitech.com/en-us/product/c930e-webcam) into the USB port on the Raspberry Pi and reboot. If everything was set up correctly, the light on the webcam should eventually illuminate, signalling that the PI Node is ready to go.

## VR Setup
This section varies slightly depending on which VR solution is being used. However, the steps remain mostly the same.
* Download Gizmo VR Player for the platform that you are using.
* Connect the device to the roboARM WiFi network.
* Navigate to the Web Browser portion of the application.
* Enter `http://[IP_OF_PI]:8080/?action=stream`
**NOTE:** It is possble to also add a hosts entry for the PI on this device as well following the same instructions as the PC. In this case the url becomes `http://roboARM:8080/?action=stream`

## Running System after setup is complete
* Plug in Robot, this should initialize everything automatically. Just wait for the webcam light to illuminate.
* Connect VR headset as shown in the previous section.
* Start PC_NODE
	* Connect to roboARM WiFi.
	* Open a terminal in `MRL_PC` and run `sudo ./leapd` (after controller is connected to the PC)
	* Open another terminal tab and run `./Start_PC.sh`

## Modifying Source code
* Navigate to the `MRL_SOURCE` folder with your favorite text editor.
* Explore, read documentation, etc.
	* For example, the files we modified were in the [myrobotlab/src/org/myrobotlab/service/](https://github.com/nickschiffer/VR-Robotic-Arm-SP/blob/master/MRL/SOURCE/myrobotlab/src/org/myrobotlab/service/) folder and included [InMoov.java](https://github.com/nickschiffer/VR-Robotic-Arm-SP/blob/master/MRL/SOURCE/myrobotlab/src/org/myrobotlab/service/InMoov.java), [InMoovArm.java](https://github.com/nickschiffer/VR-Robotic-Arm-SP/blob/master/MRL/SOURCE/myrobotlab/src/org/myrobotlab/service/InMoovArm.java), [InMoovHand.java](https://github.com/nickschiffer/VR-Robotic-Arm-SP/blob/master/MRL/SOURCE/myrobotlab/src/org/myrobotlab/service/InMoovHand.java), and [LeapMotion.java](https://github.com/nickschiffer/VR-Robotic-Arm-SP/blob/master/MRL/SOURCE/myrobotlab/src/org/myrobotlab/service/LeapMotion.java).
* Then, download `ant`, `ivy`, and `jdk8`.
* Run `ant jar` to recompile the `myrobotlab.jar` runtime executable.
* Place this file in the `MRL_PC` and `MRL_PI` folders, replacing the older version.
