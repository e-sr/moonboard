#!/bin/bash
/usr/bin/python3  /home/pi/moonboard/run.py --led_layout=evo --debug --driver SimPixel $1 2>&1 > /var/log/moonboard
