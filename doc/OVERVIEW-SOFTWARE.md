# Overview - Software used in this project


## Software Build Instructions

* Flash a fresh Raspian buster 
* run installer
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/8cH9azbsFifZ/moonboard/master/install/install.sh)"
```

## Software description

* The LEDs are driven by a raspberry using the SPI interface and the [bibliopixel]() python library. 
* The BLE of the raspberry is setup to act as the moonboard led box. When a problem is sent from the app to the raspberry a signal containing the problems holds is send on the dbus.
 More details in the `ble` folder [The BLE Process](ble/README.md).
* The LED driving process: This process listen on the dbus for new problem signals and display the problem on the strips when new problems are available. 
 This part is implemented on the script `run.py`.
 To have the script running at startup a systemd service has to be started. See `scripts/run.sh` and `services/moonbard.service`.



# Moonboard Service
To stop / restart the moonboard services (i.e. for debugging) use systemctl:
+ `sudo systemctl stop moonboard.service`
+ Debug the BLE backend using `journalctl -fu com.moonboard`
+ Debug the application itself using `tail -f /var/log/moonboard`

# LED Driver
*** FIXME ***

The LED driver scripts are located in the folder LED. moonboard.py is invoked by the BLE service. Alternatively you can run moonboard.py directly, i.e. for LED strip installation or hold setup. 
