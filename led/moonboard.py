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

# FIXME: Describe Layouts 
# FIXME: Delete this
LED_LAYOUT = {
    'nest':[
    # Top panel
    [137, 138, 149, 150, 161, 162, 173, 174, 185, 186, 197],
    [136, 139, 148, 151, 160, 163, 172, 175, 184, 187, 196],
    [135, 140, 147, 152, 159, 164, 171, 176, 183, 188, 195],
    [134, 141, 146, 153, 158, 165, 170, 177, 182, 189, 194],
    [133, 142, 145, 154, 157, 166, 169, 178, 181, 190, 193],
    [132, 143, 144, 155, 156, 167, 168, 179, 180, 191, 192],
    # Middle panel
    [131, 120, 119, 108, 107, 96, 95, 84, 83, 72, 71],
    [130, 121, 118, 109, 106, 97, 94, 85, 82, 73, 70],
    [129, 122, 117, 110, 105, 98, 93, 86, 81, 74, 69],
    [128, 123, 116, 111, 104, 99, 92, 87, 80, 75, 68],
    [127, 124, 115, 112, 103, 100, 91, 88, 79, 76, 67],
    [126, 125, 114, 113, 102, 101, 90, 89, 78, 77, 66],
    # Bottom panel
    [5, 6, 17, 18, 29, 30, 41, 42, 53, 54, 65],
    [4, 7, 16, 19, 28, 31, 40, 43, 52, 55, 64],
    [3, 8, 15, 20, 27, 32, 39, 44, 51, 56, 63],
    [2, 9, 14, 21, 26, 33, 38, 45, 50, 57, 62],
    [1, 10, 13, 22, 25, 34, 37, 46, 49, 58, 61],
    [0, 11, 12, 23, 24, 35, 36, 47, 48, 59, 60]],

'evo': [[ 17,  18,  53,  54,  89,  90, 125, 126, 161, 162, 197],
       [ 16,  19,  52,  55,  88,  91, 124, 127, 160, 163, 196],
       [ 15,  20,  51,  56,  87,  92, 123, 128, 159, 164, 195],
       [ 14,  21,  50,  57,  86,  93, 122, 129, 158, 165, 194],
       [ 13,  22,  49,  58,  85,  94, 121, 130, 157, 166, 193],
       [ 12,  23,  48,  59,  84,  95, 120, 131, 156, 167, 192],
       [ 11,  24,  47,  60,  83,  96, 119, 132, 155, 168, 191],
       [ 10,  25,  46,  61,  82,  97, 118, 133, 154, 169, 190],
       [  9,  26,  45,  62,  81,  98, 117, 134, 153, 170, 189],
       [  8,  27,  44,  63,  80,  99, 116, 135, 152, 171, 188],
       [  7,  28,  43,  64,  79, 100, 115, 136, 151, 172, 187],
       [  6,  29,  42,  65,  78, 101, 114, 137, 150, 173, 186],
       [  5,  30,  41,  66,  77, 102, 113, 138, 149, 174, 185],
       [  4,  31,  40,  67,  76, 103, 112, 139, 148, 175, 184],
       [  3,  32,  39,  68,  75, 104, 111, 140, 147, 176, 183],
       [  2,  33,  38,  69,  74, 105, 110, 141, 146, 177, 182],
       [  1,  34,  37,  70,  73, 106, 109, 142, 145, 178, 181],
       [  0,  35,  36,  71,  72, 107, 108, 143, 144, 179, 180]]
       }

class MoonBoard:
    DEFAULT_PROBLEM_COLORS = {'START':COLORS.blue,'TOP':COLORS.red,'MOVES':COLORS.green}
    DEFAULT_COLOR = COLORS.blue #FIXME ?
    X_GRID_NAMES = string.ascii_uppercase[0:11] # FIXME: del
    LED_SPACING = 3 # Use every n-th LED only - used for 3 x 4x5 LED strp      # FIXME: normal=1
    ROWS = 18 
    COLS = 11
    NUM_PIXELS = ROWS*COLS * LED_SPACING
    DEFAULT_BRIGHTNESS = 100 # FIXME: to config file
    SETUP = 'MoonboardMasters2017' # FIXME: to config file / Arg

    
    # FIXME: json
    MAPPING= { }

    with open('/home/pi/moonboard/led/led_mapping.json') as json_file:
        data = json.load(json_file)
        MAPPING = data


    def __init__(self, driver_type, led_layout=None, brightness=DEFAULT_BRIGHTNESS):
        try:
            if driver_type == "PiWS281x":
                driver = PiWS281X(self.NUM_PIXELS)
            elif driver_type == "WS2801":
                driver = WS2801(self.NUM_PIXELS, dev='/dev/spidev0.1',spi_interface= SPI_INTERFACES.PERIPHERY,spi_speed=1)
            elif driver_type == "SimPixel":
                driver = SimPixel(self.NUM_PIXELS)
                driver.open_browser()
            else:
                raise ValueError("driver_type {driver_type} unknow.".format(driver_type) )
        except (ImportError, ValueError) as e:
            print("Not able to initialize the driver. Error{}".format(e))
            print("Use bibliopixel.drivers.dummy_driver")
            driver = DriverDummy(self.NUM_PIXELS)

        if led_layout is not None:
            self.layout = Strip (driver, brightness=brightness,threadedUpdate=True)
        else:
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

    # run all colors in led´s to see if something is missing
    def led_test(self):
        print('led test')
        duration = 0.4
        COLORS = ['red', 'green', 'blue']

        for color in range(len(COLORS)):
            for i in range(1,self.ROWS+1):
                for j in range (0,self.COLS):
                    le = chr(j+65)
                    h = le+str(i)
                    #print (h)
                    self.layout.set(self.MAPPING[h], COLORS[color])
                self.layout.push_to_driver()
                time.sleep(duration)

        time.sleep (1.2)
        self.clear()


    def run_animation(self, run_options={}, **kwds): # FIXME: will it still work?
        duration = 0.001

        for i in range(1,self.ROWS+1):
            for j in range (0,self.COLS):

                le = chr(j+65)
                h = le+str(i)
                print (h)
                self.layout.set(self.MAPPING[h], COLORS.purple)
                self.layout.set(self.MAPPING[h], COLORS.blue)
                self.layout.set(self.MAPPING[h], COLORS.red)
            self.layout.push_to_driver()
            time.sleep(duration)
    
        time.sleep(60*10)

        self.clear()
        
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


class TestAnimation:
    COLOR=[COLORS.Green, COLORS.Blue]
    def __init__(self, layout, ):
        self.layout = layout

    def step(self, amt=1):
        pass

if __name__=="__main__":
    import argparse
    import time
    import subprocess

    parser = argparse.ArgumentParser(description='Test led system')

    parser.add_argument('--driver_type', type=str,
                        help='driver type, depends on leds and device controlling the led.',choices=['PiWS281x', 'WS2801', 'SimPixel'],
                        default = "PiWS281x")
    parser.add_argument('--duration',  type=int, default=10,
                        help='Delay of progress.')
    parser.add_argument('--holdset',  type=str, help="Display a holdset for current layout", 
                        choices=['Hold Set A', 'Hold Set B', 'Hold Set C', 'Original School Holds', "Wooden Holds"],
                        default = "Hold Set A")
    args = parser.parse_args()
        
    led_layout = None

    MOONBOARD = MoonBoard(args.driver_type,led_layout )
    
    # Display a holdset
    MOONBOARD.display_holdset(args.holdset, args.duration)

    print("Run animation,")
    MOONBOARD.run_animation() # FIXME

    print(f"wait {args.duration} seconds,")
    time.sleep(args.duration)
    print("clear and exit.")
    MOONBOARD.clear()