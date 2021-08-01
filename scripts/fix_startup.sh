#!/bin/bash
sudo systemctl stop moonboard
sudo systemctl stop com.moonboard
sudo systemctl restart com.moonboard
sudo systemctl restart moonboard

#sudo /usr/bin/python3  /home/pi/moonboard/run.py --debug --driver PiWS281x 