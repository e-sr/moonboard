# -*- coding: utf-8 -*-
from bibliopixel import Strip
from bibliopixel.drivers.SPI.WS2801 import  WS2801
from bibliopixel.drivers.PiWS281X import  PiWS281X
from bibliopixel.drivers.dummy_driver import DriverDummy
from bibliopixel.drivers.SimPixel import SimPixel 
from bibliopixel.colors.colors import COLORS
import string
from bibliopixel.drivers.spi_interfaces import SPI_INTERFACES
BRIGHTNESS = 100
X_GRID_NAMES = string.ascii_uppercase[0:11]
MOONBOARD_PIXELS_COUNT = 198
HOLDS_COLORS = {'START':COLORS.green,'TOP':COLORS.red,'MOVES':COLORS.blue}

def init_pixels(type, npixels = MOONBOARD_PIXELS_COUNT, brightness=BRIGHTNESS):
    driver = PiWS281X(50)

    layout = Strip(driver,  brightness=brightness)
    #layout.start()
    return layout

def coordinate_to_p_number(hold_coord, offset):
    #split coordinate in x and y grid names
    x=X_GRID_NAMES.index(hold_coord[0])
    y=int(hold_coord[1:])-1
    u = (1-(-1)**x)/2
    return int(offset + (x*18 + ((1-2*u)*y - u)%18))

def clear_problem(pixels):
    pixels.all_off()
    pixels.update()


def show_problem(pixels, holds, hold_colors = {} , offset=0, brightness=BRIGHTNESS):
    """show problem on moonboardpixels"""
    clear_problem(pixels)
    for k in ['START', 'MOVES', 'TOP']:
        for hold in holds[k]:
            pixels.set(coordinate_to_p_number(hold, offset), hold_colors.get(k, HOLDS_COLORS[k]))
    pixels.update()
    #pixels.setMasterBrightness(brightness)

def test_leds(pixels, log_func , sleep_func, duration = 20.0, color = COLORS.red):
    """"""
    npixels = pixels.numLEDs
    log_func({'progress': 0,'report': 'start test'})
    npixelsON = 18
    p=0
    for p in range(npixels+npixelsON):
        if p>=1:
            pixels.setOff(p - npixelsON)
        if p <= npixels:
            pixels.set(p, color)
        pixels.update()
        sleep_func(float(duration)/npixels)
        log_func({'progress': int(p*100/(npixels+npixelsON)), 'report': "Test running...\nLed number {}.".format(p)})
    clear_problem(pixels)
    log_func({'progress': 100, 'report': "Test finish...\nLed number {}.",'done':True})

if __name__=="__main__":
    print("Test MOONBOARD LEDS\n===========")
    import argparse
    import time
    parser = argparse.ArgumentParser(description='Test led system')

    parser.add_argument('type', type=str,
                        help='led type',choices=['WS281x', 'WS2801', 'dummy','simPixel'])
    parser.add_argument('--duration',  type=float, default=10.0,
                        help='Delay of progress.')
    parser.add_argument('--ledoffset', type=int, default=0,
                    help='number of leds on starting from 0')

    args = parser.parse_args()
    npixels=MOONBOARD_PIXELS_COUNT + args.ledoffset

    pixels = init_pixels(args.type, npixels = npixels)
    
    print("Start Led Test.")
    def f(s):
        print(s)
    test_leds(pixels=pixels, log_func=f, sleep_func=time.sleep, duration= args.duration)
    print("Exit")





