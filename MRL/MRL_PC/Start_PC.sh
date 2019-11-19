#!/bin/bash

# This script starts all of the PC node components.
# In order for this to work, you need to make a symbolic link to the LeapMotion
# daemon. To do this, run `sudo ln -s ./LEAPMOTION/data/usr/sbin/leapd .`
# Additionally, to run as non-root, run `sudo chown -R [your_username] /var/.Leap\ Motion/`.

ping -c 1 -w 2 roboARM &> /dev/null
armUp=$?

leapcount=$(pgrep -c leapd)
runMRL=0
if [[ $leapcount -lt 1 ]] ; then
    echo "INFO: leapd is not running, attempting to start now" >&2
    ./leapd --run &
    sleep 5

    leapstarted=$(pgrep -c leapd)
    if [[ $leapstarted -lt 1 ]] ; then
        echo "ERROR: Unable to start leap daemon (leapd)" >&2
        let runMRL=1
    else
	    echo "INFO: leapd successfully started, proceeding..." >&2
    fi
fi

if [[ $armUp -ne 0 ]] ; then
    echo "ERROR: RoboARM is unreachable" >&2
    let runMRL=1
fi

if [[ $runMRL -lt 1 ]] ; then
    echo "leapd appears to be running."
    echo "RoboARM appears to be reachable"
    java -jar ./myrobotlab.jar -invoke python execFile ./nickscripts/control_node.py -service GUIService GUIService SwingGui SwingGui python Python
fi
# java -jar myrobotlab.jar -invoke python -service GUIService GUIService SwingGui SwingGui python Python Arduino Arduino Servo Servo
