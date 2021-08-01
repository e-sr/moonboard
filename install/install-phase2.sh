#!/bin/bash
# FIXME: installdir
echo "Install DBUS service"
sudo cp /home/pi/moonboard/ble/com.moonboard.conf /etc/dbus-1/system.d
cd /home/pi/moonboard/ble
sudo /home/pi/moonboard/services/install_service.sh com.moonboard.service > /tmp/moonboard-service-install.log


sudo systemctl enable com.moonboard
sudo systemctl enable moonboard.service

# Remove phase 2 from boot
sudo systemctl disable moonboard-install.service
sudo systemctl start moonboard.service 
