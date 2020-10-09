# moonboard

This project contains software and informations to build a led system for a DIY MOONBOARD using a raspberrypi.

## Getting Started
* Flash a fresh Raspian buster 
* run installer
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/8cH9azbsFifZ/moonboard/master/install.sh)"
```

* Starts the application (NB: please enable spi in config.txt)


# Description

The [moonboard](https://www.moonboard.com/) smartphone app is build to work with the [moonboard led box](https://moonclimbing.com/moonboard-led-system.html) togheter (via BLE) for displaying the problems. In this project we emulate the behaviour of the box using a rasperry pi with integrated blueooth. 

## LED stripes

The led used are **addressable LED** stripes. There are many type of them: ws281x, ws2801, apa102,...  

I use WS2801(4 wires with clock line) led, buyed on Aliexpress. There are plenty of suppliers. For the Mooonboard a led spacing of at last 20cm is necessary. I asked the supplier to produce the led with a custom lenght of 23 cm. I get the leds for about 25$/50pcs.   

You  will also need a powersupply to power the leds 
The led are wired directly to the raspberry without level shifting.

The led are driven by a raspberry using the SPI interface and the [bibliopixel]() python library. 


## Hardware used

- Rapi W Zero. 
- 200 ws2801 LED 
- power supply [meanwell mdr-60-5](https://www.meanwell.com/webapp/product/search.aspx?prod=MDR-60)

## Software description

### BLE process

The BLE of the raspberry is setup to act as the moonboard led box. When a problem is sent from the app to the raspberry a signal containing the problems holds is send on the dbus.
More details in the `ble` folder.

### Led driving process

This process listen on the dbus for new problem signals and display the problem on the strips when new problems are available. This part is implemented on the script `run.py`.

To have the script running at startup a systemd service has to be started. See `scripts/run.sh` and `services/moonbard.service`.
