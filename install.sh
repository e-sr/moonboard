#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get -y install git vim python3-pip libatlas-base-dev

git clone https://github.com/8cH9azbsFifZ/moonboard.git
cd moonboard
pip3 install -r requirements.txt
pip3 install spidev
