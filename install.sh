#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get -y install git vim python3-pip
sudo apt-get -y install libatlas-base-dev
sudo apt-get -y install python-dev swig scons


git clone https://github.com/8cH9azbsFifZ/moonboard.git
cd moonboard
git pull
pip3 install -r requirements.txt
pip3 install spidev python-periphery
# FIXME
sudo pip3 install -r requirements.txt 
sudo pip3 install spidev python-periphery

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

echo "Prepare WS2811 drivers"
cd
#git clone https://github.com/jgarff/rpi_ws281x.git # use own fork for version consistency
git clone https://github.com/8cH9azbsFifZ/rpi_ws281x.git
cd rpi_ws281x
sudo scons
cd python
sudo python3 setup.py build install
cd
pip3 install rpi-ws281x 
#FIXME
sudo pip3 install rpi-ws281x 

echo "Prepare BiblioPixel Fix for WS2811"
pip3 uninstall BiblioPixel
cd
git clone https://github.com/8cH9azbsFifZ/BiblioPixel.git # use own fork for version consistency
cd BiblioPixel

python3 setup.py build
sudo python3 setup.py install


#sudo /usr/bin/python3  /home/pi/moonboard/run.py --led_layout=evo --debug --driver PiWS281x
