# moonboard

This project contains software and informations to build a home climbing wall with LED support compatible with the popular moonboard. 
This fork has been done while building my home climbing wall. 

The [moonboard](https://www.moonboard.com/) smartphone app is build to work with the [moonboard led system](https://moonclimbing.com/moonboard-led-system.html) using bluetooth low energy.
In this project we emulate the behaviour of the box using a rasperry pi and addressable LED stripes. 



# Requirements

Besides the tools, time and money (the clmbing holds are the most expensive component) you will need:

- Rapi W Zero with 8GB SD Card - powered over GPIO
- 4x LED Strip: 50x WS2811 LED, 5V, 12mm - custom cable length of 23cm
- power supply [meanwell mdr-60-5](https://www.meanwell.com/webapp/product/search.aspx?prod=MDR-60) - (~60mA * 50 * 4 = 12A ==> 60 W for 5V)
- Suitable Case (i.e. TEKO)
- Home Climbing Wall


# Build Instructions

- [How to Build a Home Climbing Wall](doc/BUILD-WALL.md)



### LED stripes

The LEDs used are **addressable LED** stripes. There are many type of them (i.e. ws281x, ws2801, apa102). The original project goes for WS2801, but they were not available in Q4 2020 for me. 
Therefore this project uses WS2811. 

The led are driven by a raspberry using the SPI interface and the [bibliopixel]() python library. 

#### Wiring the LED stripes
The WS2811 LED strips have three wires (colors may differ in your case): 
- White = GND
- Red = 5V
- Green = Signal 

Further readings:
- [Raspberry Pi Zero als LED Strip Controller](https://developer-blog.net/raspberry-pi-zero-als-led-strip-controller)



# Software Build Instructions


## Getting Started
* Flash a fresh Raspian buster 
* run installer
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/8cH9azbsFifZ/moonboard/master/install.sh)"
```

* Starts the application (NB: please enable spi in config.txt)

## Test run
```
# python3 ./run.py --driver SimPixel --debug
```
or with WS2811 LED (must run as root)
```
sudo /usr/bin/python3  /home/pi/moonboard/run.py --led_layout=evo --debug --driver PiWS281x
```



## Software description

### BLE process

The BLE of the raspberry is setup to act as the moonboard led box. When a problem is sent from the app to the raspberry a signal containing the problems holds is send on the dbus.
More details in the `ble` folder.

### Led driving process

This process listen on the dbus for new problem signals and display the problem on the strips when new problems are available. This part is implemented on the script `run.py`.

To have the script running at startup a systemd service has to be started. See `scripts/run.sh` and `services/moonbard.service`.



