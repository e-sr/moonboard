# moonboard
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


Free standing foldaway version of moonboard. Moonboard with 150mm kicker and total height of 2900mm, some alteration for 2016 hold setup needs to be done since one hold cannot fit in shortened top panel.

***WIP: Installation script not tested, otherwise working... Check different led mappings in LED folder!
TODO:Config.json for board configuration, remove old config features from code, create different led layout options ***

![MB folded away](/doc/MB-front-folded.JPG)
![MB unfolded ready to train](/doc/MB-front-unfolded.JPG)

The [moonboard](https://www.moonboard.com/) smartphone app is build to work with the [moonboard led system](https://moonclimbing.com/moonboard-led-system.html) using bluetooth low energy.
In this project we emulate the behaviour of the box using a rasperry pi and addressable LED stripes.

# Requirements

- Raspi 3 b +
- 4x LED Strips: 50x WS2811 LED, 5V, 12mm - custom cable length of 23cm (alternatively 3x 4x LED Strips with standard length of 7cm, use mooboard/led/create_nth_led_layout.py to create custom spacing for LED´s).
Ask for alibaba supplier mo make custom one.
- Power supply [meanwell mdr-60-5](https://www.meanwell.com/webapp/product/search.aspx?prod=MDR-60) - (~60mA * 50 * 4 = 12A ==> 60 W for 5V)
- DIN rail case for rpi


# Build Instructions

todo : drawing´s for the board
- [Software Description](doc/OVERVIEW-SOFTWARE.md)
