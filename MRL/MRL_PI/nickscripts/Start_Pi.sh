#!/bin/bash

# If there are lingering java processes, 
# we need to kill them so that the websockets will be released
ps aux | grep [j]ava | awk '{print $2}' | xargs kill

# Check if mjpg-streamer is already running. If not, we need to
# start it
mjpg_running=$(pgrep -c mjpg)
if [[ $mjpg_running -lt 1 ]] ; then
    echo "mjpg-streamer not running, starting now..." >&2
    #/usr/local/bin/mjpg_streamer -i "input_uvc.so -r 1920x1080 -d /dev/video0 -f 24 -q 80" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www" &
    /usr/local/bin/mjpg_streamer -i "input_uvc.so -r 1080x720 -d /dev/video0 -f 24 -q 80" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www" &
fi

# Start MRL and any needed services, then invoke the python script
java -jar ../myrobotlab.jar -service python Python -invoke python execFile ./nickscripts/Remote_inMoov_arm.py &

# Renice so this runs at a higher priority
#sudo renice -n -10 -u nick
