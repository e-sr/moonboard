# -*- coding: utf-8 -*-
from bibliopixel.colors import COLORS
from bibliopixel import Matrix
from bibliopixel.drivers.PiWS281X import PiWS281X
from bibliopixel.drivers.dummy_driver import DriverDummy
from bibliopixel.drivers.SPI.WS2801 import  WS2801
from bibliopixel.drivers.SimPixel import SimPixel
from bibliopixel.drivers.spi_interfaces import SPI_INTERFACES
import string
import json



# FIXME: Describe Layouts
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
       [  0,  35,  36,  71,  72, 107, 108, 143, 144, 179, 180]],

'gz': 
[[51, 54, 159, 162, 267, 270, 375, 378, 483, 486, 591], [48, 57, 156, 165, 264, 273, 372, 381, 480, 489, 588], [45, 60, 153, 168, 261, 276, 369, 384, 477, 492, 585], [42, 63, 150, 171, 258, 279, 366, 387, 474, 495, 582], [39, 66, 147, 174, 255, 282, 363, 390, 471, 498, 579], [36, 69, 144, 177, 252, 285, 360, 393, 468, 501, 576], [33, 72, 141, 180, 249, 288, 357, 396, 465, 504, 573], [30, 75, 138, 183, 246, 291, 354, 399, 462, 507, 570], [27, 78, 135, 186, 243, 294, 351, 402, 459, 510, 567], [24, 81, 132, 189, 240, 297, 348, 405, 456, 513, 564], [21, 84, 129, 192, 237, 300, 345, 408, 453, 516, 561], [18, 87, 126, 195, 234, 303, 342, 411, 450, 519, 558], [15, 90, 123, 198, 231, 306, 339, 414, 447, 522, 555], [12, 93, 120, 201, 228, 309, 336, 417, 444, 525, 552], [9, 96, 117, 204, 225, 312, 333, 420, 441, 528, 549], [6, 99, 114, 207, 222, 315, 330, 423, 438, 531, 546], [3, 102, 111, 210, 219, 318, 327, 426, 435, 534, 543], [0, 105, 108, 213, 216, 321, 324, 429, 432, 537, 540]]
       
       }

class MoonBoard:
    DEFAULT_PROBLEM_COLORS = {'START':COLORS.blue,'TOP':COLORS.red,'MOVES':COLORS.green}
    DEFAULT_COLOR = COLORS.blue #FIXME ?
    X_GRID_NAMES = string.ascii_uppercase[0:11]
    LED_SPACING = 3 # Use every n-th LED only - used for 3 x 4x5 LED strp      # FIXME: normal=1
    ROWS = 18
    COLS = 11
    NUM_PIXELS = ROWS*COLS*LED_SPACING 
    DEFAULT_BRIGHTNESS = 150 # FIXME: to config file
    SETUP = 'Moonboard2016' # FIXME: to config file / Arg


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
            self.layout = Matrix(driver,
                                width=self.COLS,
                                height=self.ROWS*self.LED_SPACING,
                                coord_map=led_layout,
                                threadedUpdate=True,
                                brightness=brightness
                                )
        else:
            self.layout = Matrix(driver,width=11,height=self.ROWS*self.LED_SPACING, 
                                threadedUpdate=True,
                                brightness=brightness
                                )
        self.layout.cleanup_drivers()
        self.layout.start()
        self.animation = None

    def clear(self):
        self.stop_animation()
        self.layout.all_off()
        self.layout.push_to_driver()

    def set_hold(self, hold, color=DEFAULT_COLOR):
        x_grid_name, y_grid_name = hold[0], int(hold[1:])
        x = self.X_GRID_NAMES.index(x_grid_name)
        y = (self.ROWS - y_grid_name) * self.LED_SPACING # FIXME
        self.layout.set(x, y, color)

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

    def run_animation(self, run_options={}, **kwds): # FIXME: will it still work?
        duration = 0.01
        #all_holds = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'I11', 'I12', 'I13', 'I14', 'I15', 'I16', 'I17', 'I18', 'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10', 'J11', 'J12', 'J13', 'J14', 'J15', 'J16', 'J17', 'J18', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'K10', 'K11', 'K12', 'K13', 'K14', 'K15', 'K16', 'K17', 'K18']
        #for h in all_holds:
        #    self.set_hold (h, COLORS.blue)
        #    self.layout.push_to_driver()
        # 
        #    time.sleep(duration)

        #for r in range (0, self.ROWS):
        #    for c in range (0, self.COLS):
        #        color= COLORS.blue
        #        self.layout.set(r, c, color)
        #        self.layout.push_to_driver()
        #        time.sleep(duration)

        #self.show_hold("A1", color=COLORS.red)

        with open('../problems/HoldSetup.json') as json_file: # FIXME: path 
            data = json.load(json_file)
            for hold in data[self.SETUP]:
                holdset = (data[self.SETUP][hold]['HoldSet']) # A, B, OS for 2016 
                color = COLORS.yellow
                if (holdset == "A"):
                    color = COLORS.red
                if (holdset == "B"):
                    color = COLORS.blue
                if (holdset == "OS"):
                    color = COLORS.yellow

                self.set_hold (hold, color)
                self.layout.push_to_driver()
                #print "Orientation"

                time.sleep(duration)

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

    parser.add_argument('driver_type', type=str,
                        help='driver type, depends on leds and device controlling the led.',choices=['PiWS281x', 'WS2801', 'SimPixel'])
    parser.add_argument('--duration',  type=int, default=10,
                        help='Delay of progress.')
    parser.add_argument('--special_nest_layout',  action='store_true')
    args = parser.parse_args()
        
    print("Test MOONBOARD LEDS\n===========")
    led_layout = LED_LAYOUT['nest'] if args.special_nest_layout else None
    MOONBOARD = MoonBoard(args.driver_type,led_layout )
    print("Run animation,")
    #animation=
    MOONBOARD.run_animation()
    #MOONBOARD.layout.fillScreen(COLORS.red)
    print(f"wait {args.duration} seconds,")
    time.sleep(args.duration)
    print("clear and exit.")
    MOONBOARD.clear()