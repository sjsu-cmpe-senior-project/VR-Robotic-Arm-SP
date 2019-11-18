#!/bin/bash

# You need to configure this script to run at boot. In this case
# we are using DietPi OS. You can run `dietpi-autostart` and select
# custom script. Then, place this file in `/var/lib/dietpi/dietpi-autostart/`
# and rename to `custom.sh`.

# Need to wait for router to boot up
printf "%s" "waiting for network ..."
while ! ping -c 1 -n -w 1 192.168.1.1 &> /dev/null
do
    printf "%c" "."
done
printf "\n%s\n"  "Network is Connected, starting roboARM"

# Once the router is up, we can run the startup script
# with high priority
cd /home/nick/MRL/nickscripts
nice -n -10 ./Start_Pi.sh &
