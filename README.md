# moonboard

This project contains software and informations to build a home climbing wall with LED support compatible with the popular moonboard. This fork has been done while building my home climbing wall.

## Description

The [moonboard](https://www.moonboard.com/) smartphone app is build to work with the [moonboard led box](https://moonclimbing.com/moonboard-led-system.html) togheter (via BLE) for displaying the problems. 
In this project we emulate the behaviour of the box using a rasperry pi with integrated blueooth. 


# Climbing Wall Build Instructions
When it comes to home build system walls, there is lots of information on the web these days. Most widely known is the moonboard (other brands as tension or kelter 
board are available, too). It seems like the pattern of 18 rows and 11 columns is most famous, as it has been adapted by the other brands as well. 

## General Considerations

My boundary conditions for the construction of my home climbing wall were: 
- it should used my available space as best as possible (roof), 
- I should be able to do all work on my own without help (including transportation of the wood), 
- the build process must be iterative due to my time constraints (spread out over 7 months),
- I have to rely on other hold sources (delivery bottle neck due to lockdowns)

Popular angles for a home climbing wall are 20° and 40°. The angle of my roof is about 40°, so I had to go for the harder version. 
A thing to consider in advance 
[Training Log Day 2 - Power | Moonboard | 25° & 40° Comparison](https://www.youtube.com/watch?v=wOz9GRdQMNc&feature=youtu.be&ab_channel=AlternativeBeta)
and 
[How and why to train on a moonboard](https://www.climbing.com/skills/how-and-why-to-train-on-the-moonboard/).




## Design the dimensions
After measuring my room in the rooftop I drew a lot of different alternatives where to locate the board and what sizes to choose. 
Dimensions like size of wood, wall, angle, overlap, drill spacings etc. can easily be calculated using an excel sheet (TBD).

Ben Moon himself is cited: "As you have pointed out you could reduce the kick board hight and eliminate the rows although this isn’t a good idea. 
Your best option is to keep all the rows but reduce the spacing between rows. This means you can do all the problems listed on the website but they will be at a slightly easier grade." 
[Forum Post](https://www.mountainproject.com/forum/topic/109397643/moon-board-modifications).



# LED Build Instructions

## Hardware used

- Rapi W Zero with 8GB SD Card - powered over GPIO
- 4x LED Strip: 50x WS2811 LED, 5V, 12mm - custom cable length of 23cm
- power supply [meanwell mdr-60-5](https://www.meanwell.com/webapp/product/search.aspx?prod=MDR-60) - (~60mA * 50 * 4 = 12A ==> 60 W for 5V)
- Suitable Case (i.e. TEKO)


### LED stripes

The LEDs used are **addressable LED** stripes. There are many type of them (i.e. ws281x, ws2801, apa102). The original project goes for WS2801, but they were not available in Q4 2020 for me. 
Therefore this project uses WS2811. 


The led are driven by a raspberry using the SPI interface and the [bibliopixel]() python library. 

Further readings:
- https://developer-blog.net/raspberry-pi-zero-als-led-strip-controller



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



