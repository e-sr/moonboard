#!/bin/bash
set -o errexit
LOG_FILE=/var/log/moonboard

exec 1>$LOG_FILE
exec 2>&1

sudo /usr/bin/python3  /home/pi/moonboard/run.py --debug --driver=PiWS281x --led_layout=nest $1 
