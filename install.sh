#!/bin/bash

#echo blacklist snd_bcm2835 >> /etc/modprobe.d/raspi-blacklist.conf
#/boot/config.txt
##dtparam=audio=on
# FIXME - stuff for spi
# FIXME - provide as patch
# * Starts the application (NB: please enable spi in config.txt)


# Install dependencies
sudo apt-get update
sudo apt-get upgrade
sudo apt-get -y install git vim python3-pip gcc make build-essential
sudo apt-get -y install libatlas-base-dev 
sudo apt-get -y install python-dev swig scons # for building WS2811 drivers

# Installing moonboard code
git clone https://github.com/8cH9azbsFifZ/moonboard.git
cd moonboard
git pull

# Installing python dependencies
pip3 install -r requirements.txt
sudo pip3 install -r requirements.txt 
# pip3 uninstall -y -r requirements.txt # uninstall


echo "Prepare BiblioPixel Fix for WS2811 (Python)"
cd /usr/local/lib/python3.7/dist-packages/bibliopixel/drivers/
sudo patch < ~/moonboard/patch/PiWS281X.py.patch 
cd


echo "Install service"
cd services
sudo ./install_service.sh moonboard.service 
cd ..


echo "Install DBUS service"
sudo cp ble/com.moonboard.conf /etc/dbus-1/system.d
sudo cp ble/com.moonboard.service /usr/share/dbus-1/system-services/


echo "Start advertising stuff"
sudo hcitool -i hci0 cmd 0x08 0x0008  {adv: 32 byte 0-padded if necessary}
sudo hcitool -i hci0 cmd 0x08 0x0009 {adv: 32 byte 0-padded if necessary}
sudo hcitool -i hci0 cmd 0x08 0x0006 {min:2byte} {max:2byte} {connectable:1byte} 00 00 00 00 00 00 00 00 07 00
sudo hcitool -i hci0 cmd 0x08 0x000a 01


echo "Prepare logfiles"
sudo touch /var/log/moonboard
sudo chown pi:pi /var/log/moonboard