# moonboard
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


This project contains software and informations to build a home climbing wall with LED support compatible with the popular moonboard. 
This fork has been done while building my home climbing wall. 

***WIP: Project ongoing. Next step: stabilize the code. ***
*** => Please use the latest tagged version, :latest will probably not work for you. ***


![Image of the Wall](doc/front.png)
![LEDs](doc/led.png)

The [moonboard](https://www.moonboard.com/) smartphone app is build to work with the [moonboard led system](https://moonclimbing.com/moonboard-led-system.html) using bluetooth low energy.
In this project we emulate the behaviour of the box using a rasperry pi and addressable LED stripes. 


# Requirements

Besides the tools, time and money (the climbing holds are the most expensive component) you will need:

- Rapi W Zero with 8GB SD Card - powered over GPIO
- 4x LED Strips: 50x WS2811 LED, 5V, 12mm - custom cable length of 23cm (alternatively 3x 4x LED Strips with standard length of 7cm)
- Power supply [meanwell mdr-60-5](https://www.meanwell.com/webapp/product/search.aspx?prod=MDR-60) - (~60mA * 50 * 4 = 12A ==> 60 W for 5V)
- Suitable Case (i.e. TEKO)


# Build Instructions

- [How to Build a Home Climbing Wall](doc/BUILD-WALL.md)
- [How to Build the LED System](doc/BUILD-LEDSYSTEM.md)
- [Software Description](doc/OVERVIEW-SOFTWARE.md)
