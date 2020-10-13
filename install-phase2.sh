echo "Install DBUS service"
sudo cp /home/pi/moonboard/ble/com.moonboard.conf /etc/dbus-1/system.d
cd ble
sudo ../services/install_service.sh com.moonboard.service > /tmp/moonboard-service-install.log
cd ..

# Remove phase 2 from boot
sudo sed -i 's/sudo \/home\/pi\/moonboard\/install-phase2.sh//g' /etc/rc.local