#!/bin/bash


sudo apt-get update
sudo apt-get -y install git vim python3-pip
sudo apt-get -y install libatlas-base-dev

git clone https://github.com/e-sr/moonboard.git
cd moonboard
pip3 install -r requirements.txt
pip3 install spidev
