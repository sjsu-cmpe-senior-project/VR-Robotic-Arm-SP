#!/bin/bash

# If there are lingering java processes, 
# we need to kill them so that the websockets will be released
ps aux | grep [j]ava | awk '{print $2}' | xargs kill

# Start MRL and any needed services, then invoke the python script
java -jar ../myrobotlab.jar -service GUIService GUIservice SwingGui SwingGui python Python -invoke python execFile ./nickscripts/Remote_inMoov_arm.py &

# Renice so this runs at a higher priority
sudo renice -n -10 -u nick
