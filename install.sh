#!/bin/bash

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install git vim python3-pip libatlas-base-dev

test -d moonboard || git clone https://github.com/8cH9azbsFifZ/moonboard.git
cd moonboard
git pull
pip3 install -r requirements.txt
pip3 install spidev

cd services
sudo ./install_service.sh moonboard.service 
cd ..
