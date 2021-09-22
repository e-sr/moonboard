# -*- coding: utf-8 -*-
from bibliopixel.colors import COLORS
from bibliopixel import Strip
from bibliopixel.drivers.PiWS281X import PiWS281X
from bibliopixel.drivers.dummy_driver import DriverDummy
from bibliopixel.drivers.SPI.WS2801 import  WS2801
from bibliopixel.drivers.SimPixel import SimPixel
from bibliopixel.drivers.spi_interfaces import SPI_INTERFACES
import string
import json
import time
import os

class MoonBoard:
    DEFAULT_PROBLEM_COLORS = {'START':COLORS.blue,'TOP':COLORS.red,'MOVES':COLORS.green}
    DEFAULT_COLOR = COLORS.blue #FIXME ?
    X_GRID_NAMES = string.ascii_uppercase[0:11] # FIXME: del
    ROWS = 18 
    COLS = 11
    DEFAULT_BRIGHTNESS = 100 # FIXME: to config file
    SETUP = 'MoonboardMasters2017' # FIXME: to config file / Arg
    DEFAULT_LED_MAPPING_FILE='led_mapping.json'
    # generate with {C+str(n+1):int(i*18+ (1-((-1)**(i%2)))/2*17 + ((-1)**(i%2))*n) for  i, C in enumerate(string.ascii_uppercase[0:11]) for n in range(18) }
    def __init__(self, 
                    driver_type, 
                    led_mapping=DEFAULT_LED_MAPPING_FILE, 
                    brightness=DEFAULT_BRIGHTNESS):
        #read led mapping
        led_mappimng_abs = os.path.join(os.path.dirname(__file__), led_mapping)
        with open(led_mappimng_abs) as json_file:
            try:
                data = json.load(json_file)
            except Exception as e:
                print("Json led mapping not a valid JSON.")
                raise e
            else:
                self.MAPPING = data
        
        try:
            num_pixels=self.MAPPING["num_pixels"]
        except:
            num_pixels=max(self.MAPPING.values())+1

        try:
            if driver_type == "PiWS281x":
                driver = PiWS281X(num_pixels)
            elif driver_type == "WS2801":
                driver = WS2801(num_pixels, dev='/dev/spidev0.1',spi_interface= SPI_INTERFACES.PERIPHERY,spi_speed=1)
            elif driver_type == "SimPixel":
                driver = SimPixel(num_pixels)
                driver.open_browser()
            else:
                raise ValueError("driver_type {driver_type} unknow.".format(driver_type) )
        except (ImportError, ValueError) as e:
            print("Not able to initialize the driver. Error{}".format(e))
            print("Use bibliopixel.drivers.dummy_driver")
            driver = DriverDummy(num_pixels)

        self.layout = Strip (driver, brightness=brightness,threadedUpdate=True)
        self.layout.cleanup_drivers()
        self.layout.start()
        self.animation = None

    def clear(self):
        self.stop_animation()
        self.layout.all_off()
        self.layout.push_to_driver()

    def set_hold(self, hold, color=DEFAULT_COLOR):
        self.layout.set(self.MAPPING[hold], color)

    def show_hold(self, hold, color=DEFAULT_COLOR):
        self.set_hold(hold, color)
        self.layout.push_to_driver()

    def show_problem(self, holds, hold_colors={}):
        self.clear()
        for k in ['START', 'MOVES', 'TOP']:
            for hold in holds[k]:
                self.set_hold(
                    hold, 
                    hold_colors.get(k, self.DEFAULT_PROBLEM_COLORS[k]),
                    )
        self.layout.push_to_driver()

    def led_layout_test(self, duration, **kwds): 
        for c in self.X_GRID_NAMES:
            for j in range (1,self.ROWS+1):
                h = c+str(j)
                print (h)
                for color in [COLORS.red, COLORS.blue]:
                    self.layout.set(self.MAPPING[h], color)
                    self.layout.push_to_driver()
                    time.sleep(duration/400)
        
    def display_holdset(self, holdset="Hold Set A", duration=10, **kwds): 
        print ("Display holdset: " + str(holdset))

        with open('../problems/HoldSetup.json') as json_file: # FIXME: path 
            data = json.load(json_file)
            for hold in data[self.SETUP]:
                hs = (data[self.SETUP][hold]['HoldSet']) 
                color = COLORS.black
    
                if (hs == holdset):# FIXME
                        color = COLORS.green                    
    
                self.layout.set(self.MAPPING[hold], color)

                #self.set_hold (hold, color)
                #print "Orientation"
        
        self.layout.push_to_driver()

        wait_holdset_duration = duration # FIXME
        time.sleep(wait_holdset_duration)

        self.clear()
                
                
                
    def stop_animation(self):
        if self.animation is not None:
            self.animation.stop()


if __name__=="__main__":
    import argparse
    import time
    import subprocess

    parser = argparse.ArgumentParser(description='Test led system')

    parser.add_argument('--driver_type', type=str,
                        help='driver type, depends on leds and device controlling the led.',choices=['PiWS281x', 'WS2801', 'SimPixel'],
                        default = "PiWS281x")
    parser.add_argument('--led_mapping', type=str,
                        help='Relative path JSON file containing the led mapping.',
                        default = "led_mapping.json")                   
    parser.add_argument('--duration',  type=int, default=10,
                        help='Delay of progress.')
    parser.add_argument('--holdset',  type=str, help="Display a holdset for current layout", 
                        choices=['Hold Set A', 'Hold Set B', 'Hold Set C', 'Original School Holds', "Wooden Holds"],
                        default = "Hold Set A")
    args = parser.parse_args()
        
    led_layout = None

    MOONBOARD = MoonBoard(args.driver_type,args.led_mapping )

    print("Led Layout Test,")
    MOONBOARD.led_layout_test(args.duration) 

    # Display a holdset
    MOONBOARD.display_holdset(args.holdset, args.duration)

    print("clear and exit.")
    MOONBOARD.clear()