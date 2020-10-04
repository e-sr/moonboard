#!/bin/bash
set -o errexit
LOG_FILE=/var/log/moonboard

exec 1>>$LOG_FILE
exec 2>>&1

/usr/bin/python3  /home/pi/moonboard/run.py --led_layout=evo --debug --driver SimPixel $1 
