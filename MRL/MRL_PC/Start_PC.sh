#!/bin/bash
# ./LEAPMOTION/data/usr/sbin/leapd --usermode &
ping -c 1 roboARM &> /dev/null
armUp=$?

leapcount=$(pgrep -c leapd)
runMRL=0
if [[ $leapcount -lt 1 ]] ; then
    echo "ERROR: leapd is not running" >&2
    let runMRL=1
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
