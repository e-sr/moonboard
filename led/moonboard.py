# -*- coding: utf-8 -*-
from bibliopixel.colors import COLORS
from bibliopixel import Matrix
from bibliopixel import Strip
from bibliopixel.drivers.PiWS281X import PiWS281X
from bibliopixel.drivers.dummy_driver import DriverDummy
from bibliopixel.drivers.SPI.WS2801 import  WS2801
from bibliopixel.drivers.SimPixel import SimPixel
from bibliopixel.drivers.spi_interfaces import SPI_INTERFACES
import string
import json

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
       [  0,  35,  36,  71,  72, 107, 108, 143, 144, 179, 180]],

'gz': 
#[[53, 54, 161, 162, 269, 270, 377, 378, 485, 486, 593], [52, 55, 160, 163, 268, 271, 376, 379, 484, 487, 592], [51, 56, 159, 164, 267, 272, 375, 380, 483, 488, 591], [50, 57, 158, 165, 266, 273, 374, 381, 482, 489, 590], [49, 58, 157, 166, 265, 274, 373, 382, 481, 490, 589], [48, 59, 156, 167, 264, 275, 372, 383, 480, 491, 588], [47, 60, 155, 168, 263, 276, 371, 384, 479, 492, 587], [46, 61, 154, 169, 262, 277, 370, 385, 478, 493, 586], [45, 62, 153, 170, 261, 278, 369, 386, 477, 494, 585], [44, 63, 152, 171, 260, 279, 368, 387, 476, 495, 584], [43, 64, 151, 172, 259, 280, 367, 388, 475, 496, 583], [42, 65, 150, 173, 258, 281, 366, 389, 474, 497, 582], [41, 66, 149, 174, 257, 282, 365, 390, 473, 498, 581], [40, 67, 148, 175, 256, 283, 364, 391, 472, 499, 580], [39, 68, 147, 176, 255, 284, 363, 392, 471, 500, 579], [38, 69, 146, 177, 254, 285, 362, 393, 470, 501, 578], [37, 70, 145, 178, 253, 286, 361, 394, 469, 502, 577], [36, 71, 144, 179, 252, 287, 360, 395, 468, 503, 576], [35, 72, 143, 180, 251, 288, 359, 396, 467, 504, 575], [34, 73, 142, 181, 250, 289, 358, 397, 466, 505, 574], [33, 74, 141, 182, 249, 290, 357, 398, 465, 506, 573], [32, 75, 140, 183, 248, 291, 356, 399, 464, 507, 572], [31, 76, 139, 184, 247, 292, 355, 400, 463, 508, 571], [30, 77, 138, 185, 246, 293, 354, 401, 462, 509, 570], [29, 78, 137, 186, 245, 294, 353, 402, 461, 510, 569], [28, 79, 136, 187, 244, 295, 352, 403, 460, 511, 568], [27, 80, 135, 188, 243, 296, 351, 404, 459, 512, 567], [26, 81, 134, 189, 242, 297, 350, 405, 458, 513, 566], [25, 82, 133, 190, 241, 298, 349, 406, 457, 514, 565], [24, 83, 132, 191, 240, 299, 348, 407, 456, 515, 564], [23, 84, 131, 192, 239, 300, 347, 408, 455, 516, 563], [22, 85, 130, 193, 238, 301, 346, 409, 454, 517, 562], [21, 86, 129, 194, 237, 302, 345, 410, 453, 518, 561], [20, 87, 128, 195, 236, 303, 344, 411, 452, 519, 560], [19, 88, 127, 196, 235, 304, 343, 412, 451, 520, 559], [18, 89, 126, 197, 234, 305, 342, 413, 450, 521, 558], [17, 90, 125, 198, 233, 306, 341, 414, 449, 522, 557], [16, 91, 124, 199, 232, 307, 340, 415, 448, 523, 556], [15, 92, 123, 200, 231, 308, 339, 416, 447, 524, 555], [14, 93, 122, 201, 230, 309, 338, 417, 446, 525, 554], [13, 94, 121, 202, 229, 310, 337, 418, 445, 526, 553], [12, 95, 120, 203, 228, 311, 336, 419, 444, 527, 552], [11, 96, 119, 204, 227, 312, 335, 420, 443, 528, 551], [10, 97, 118, 205, 226, 313, 334, 421, 442, 529, 550], [9, 98, 117, 206, 225, 314, 333, 422, 441, 530, 549], [8, 99, 116, 207, 224, 315, 332, 423, 440, 531, 548], [7, 100, 115, 208, 223, 316, 331, 424, 439, 532, 547], [6, 101, 114, 209, 222, 317, 330, 425, 438, 533, 546], [5, 102, 113, 210, 221, 318, 329, 426, 437, 534, 545], [4, 103, 112, 211, 220, 319, 328, 427, 436, 535, 544], [3, 104, 111, 212, 219, 320, 327, 428, 435, 536, 543], [2, 105, 110, 213, 218, 321, 326, 429, 434, 537, 542], [1, 106, 109, 214, 217, 322, 325, 430, 433, 538, 541], [0, 107, 108, 215, 216, 323, 324, 431, 432, 539, 540]]
[[55, 56, 167, 168, 279, 280, 391, 392, 503, 504, 615], [54, 57, 166, 169, 278, 281, 390, 393, 502, 505, 614], [53, 58, 165, 170, 277, 282, 389, 394, 501, 506, 613], [52, 59, 164, 171, 276, 283, 388, 395, 500, 507, 612], [51, 60, 163, 172, 275, 284, 387, 396, 499, 508, 611], [50, 61, 162, 173, 274, 285, 386, 397, 498, 509, 610], [49, 62, 161, 174, 273, 286, 385, 398, 497, 510, 609], [48, 63, 160, 175, 272, 287, 384, 399, 496, 511, 608], [47, 64, 159, 176, 271, 288, 383, 400, 495, 512, 607], [46, 65, 158, 177, 270, 289, 382, 401, 494, 513, 606], [45, 66, 157, 178, 269, 290, 381, 402, 493, 514, 605], [44, 67, 156, 179, 268, 291, 380, 403, 492, 515, 604], [43, 68, 155, 180, 267, 292, 379, 404, 491, 516, 603], [42, 69, 154, 181, 266, 293, 378, 405, 490, 517, 602], [41, 70, 153, 182, 265, 294, 377, 406, 489, 518, 601], [40, 71, 152, 183, 264, 295, 376, 407, 488, 519, 600], [39, 72, 151, 184, 263, 296, 375, 408, 487, 520, 599], [38, 73, 150, 185, 262, 297, 374, 409, 486, 521, 598], [37, 74, 149, 186, 261, 298, 373, 410, 485, 522, 597], [36, 75, 148, 187, 260, 299, 372, 411, 484, 523, 596], [35, 76, 147, 188, 259, 300, 371, 412, 483, 524, 595], [34, 77, 146, 189, 258, 301, 370, 413, 482, 525, 594], [33, 78, 145, 190, 257, 302, 369, 414, 481, 526, 593], [32, 79, 144, 191, 256, 303, 368, 415, 480, 527, 592], [31, 80, 143, 192, 255, 304, 367, 416, 479, 528, 591], [30, 81, 142, 193, 254, 305, 366, 417, 478, 529, 590], [29, 82, 141, 194, 253, 306, 365, 418, 477, 530, 589], [28, 83, 140, 195, 252, 307, 364, 419, 476, 531, 588], [27, 84, 139, 196, 251, 308, 363, 420, 475, 532, 587], [26, 85, 138, 197, 250, 309, 362, 421, 474, 533, 586], [25, 86, 137, 198, 249, 310, 361, 422, 473, 534, 585], [24, 87, 136, 199, 248, 311, 360, 423, 472, 535, 584], [23, 88, 135, 200, 247, 312, 359, 424, 471, 536, 583], [22, 89, 134, 201, 246, 313, 358, 425, 470, 537, 582], [21, 90, 133, 202, 245, 314, 357, 426, 469, 538, 581], [20, 91, 132, 203, 244, 315, 356, 427, 468, 539, 580], [19, 92, 131, 204, 243, 316, 355, 428, 467, 540, 579], [18, 93, 130, 205, 242, 317, 354, 429, 466, 541, 578], [17, 94, 129, 206, 241, 318, 353, 430, 465, 542, 577], [16, 95, 128, 207, 240, 319, 352, 431, 464, 543, 576], [15, 96, 127, 208, 239, 320, 351, 432, 463, 544, 575], [14, 97, 126, 209, 238, 321, 350, 433, 462, 545, 574], [13, 98, 125, 210, 237, 322, 349, 434, 461, 546, 573], [12, 99, 124, 211, 236, 323, 348, 435, 460, 547, 572], [11, 100, 123, 212, 235, 324, 347, 436, 459, 548, 571], [10, 101, 122, 213, 234, 325, 346, 437, 458, 549, 570], [9, 102, 121, 214, 233, 326, 345, 438, 457, 550, 569], [8, 103, 120, 215, 232, 327, 344, 439, 456, 551, 568], [7, 104, 119, 216, 231, 328, 343, 440, 455, 552, 567], [6, 105, 118, 217, 230, 329, 342, 441, 454, 553, 566], [5, 106, 117, 218, 229, 330, 341, 442, 453, 554, 565], [4, 107, 116, 219, 228, 331, 340, 443, 452, 555, 564], [3, 108, 115, 220, 227, 332, 339, 444, 451, 556, 563], [2, 109, 114, 221, 226, 333, 338, 445, 450, 557, 562], [1, 110, 113, 222, 225, 334, 337, 446, 449, 558, 561], [0, 111, 112, 223, 224, 335, 336, 447, 448, 559, 560]]

       }

class MoonBoard:
    DEFAULT_PROBLEM_COLORS = {'START':COLORS.blue,'TOP':COLORS.red,'MOVES':COLORS.green}
    DEFAULT_COLOR = COLORS.blue #FIXME ?
    X_GRID_NAMES = string.ascii_uppercase[0:11] # FIXME: del
    LED_SPACING = 3 # Use every n-th LED only - used for 3 x 4x5 LED strp      # FIXME: normal=1
    ROWS = 18 * LED_SPACING # FIXME
    COLS = 11
    NUM_PIXELS = ROWS*COLS
    DEFAULT_BRIGHTNESS = 150 # FIXME: to config file
    SETUP = 'Moonboard2016' # FIXME: to config file / Arg

    
    # FIXME: json
    MAPPING= { }
        #'A1': 0, 'A2': 3, 'A3': 6, 'A4': 9, 'A5': 12, 'A6': 15, 'A7': 18, 'A8': 21, 'A9': 24, 'A10': 27, 'A11': 30, 'A12': 33, 'A13': 36, 'A14': 39, 'A15': 42, 'A16': 45, 'A17': 48, 'A18': 51, 'B1': 54, 'B2': 57, 'B3': 60, 'B4': 63, 'B5': 66, 'B6': 69, 'B7': 72, 'B8': 75, 'B9': 78, 'B10': 81, 'B11': 84, 'B12': 87, 'B13': 90, 'B14': 93, 'B15': 96, 'B16': 99, 'B17': 102, 'B18': 105, 'C1': 108, 'C2': 111, 'C3': 114, 'C4': 117, 'C5': 120, 'C6': 123, 'C7': 126, 'C8': 129, 'C9': 132, 'C10': 135, 'C11': 138, 'C12': 141, 'C13': 144, 'C14': 147, 'C15': 150, 'C16': 153, 'C17': 156, 'C18': 159, 'D1': 162, 'D2': 165, 'D3': 168, 'D4': 171, 'D5': 174, 'D6': 177, 'D7': 180, 'D8': 183, 'D9': 186, 'D10': 189, 'D11': 192, 'D12': 195, 'D13': 198, 'D14': 201, 'D15': 204, 'D16': 207, 'D17': 210, 'D18': 213, 'E1': 216, 'E2': 219, 'E3': 222, 'E4': 225, 'E5': 228, 'E6': 231, 'E7': 234, 'E8': 237, 'E9': 240, 'E10': 243, 'E11': 246, 'E12': 249, 'E13': 252, 'E14': 255, 'E15': 258, 'E16': 261, 'E17': 264, 'E18': 267, 'F1': 270, 'F2': 273, 'F3': 276, 'F4': 279, 'F5': 282, 'F6': 285, 'F7': 288, 'F8': 291, 'F9': 294, 'F10': 297, 'F11': 300, 'F12': 303, 'F13': 306, 'F14': 309, 'F15': 312, 'F16': 315, 'F17': 318, 'F18': 321, 'G1': 324, 'G2': 327, 'G3': 330, 'G4': 333, 'G5': 336, 'G6': 339, 'G7': 342, 'G8': 345, 'G9': 348, 'G10': 351, 'G11': 354, 'G12': 357, 'G13': 360, 'G14': 363, 'G15': 366, 'G16': 369, 'G17': 372, 'G18': 375, 'H1': 378, 'H2': 381, 'H3': 384, 'H4': 387, 'H5': 390, 'H6': 393, 'H7': 396, 'H8': 399, 'H9': 402, 'H10': 405, 'H11': 408, 'H12': 411, 'H13': 414, 'H14': 417, 'H15': 420, 'H16': 423, 'H17': 426, 'H18': 429, 'I1': 432, 'I2': 435, 'I3': 438, 'I4': 441, 'I5': 444, 'I6': 447, 'I7': 450, 'I8': 453, 'I9': 456, 'I10': 459, 'I11': 462, 'I12': 465, 'I13': 468, 'I14': 471, 'I15': 474, 'I16': 477, 'I17': 480, 'I18': 483, 'J1': 486, 'J2': 489, 'J3': 492, 'J4': 495, 'J5': 498, 'J6': 501, 'J7': 504, 'J8': 507, 'J9': 510, 'J10': 513, 'J11': 516, 'J12': 519, 'J13': 522, 'J14': 525, 'J15': 528, 'J16': 531, 'J17': 534, 'J18': 537, 'K1': 540, 'K2': 543, 'K3': 546, 'K4': 549, 'K5': 552, 'K6': 555, 'K7': 558, 'K8': 561, 'K9': 564, 'K10': 567, 'K11': 570, 'K12': 573, 'K13': 576, 'K14': 579, 'K15': 582, 'K16': 585, 'K17': 588, 'K18': 591}

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
            self.layout = Matrix(driver, # FIXmE: del
                                width=self.COLS,
                                height=self.ROWS,
                                coord_map=led_layout,
                                threadedUpdate=True,
                                brightness=brightness
                                )
        else:
            self.layout = Strip (driver) #Matrix(driver,width=self.COLS,height=self.ROWS, 
                          #      threadedUpdate=True,
                          #      brightness=brightness
                          #      )
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
# b working        y = (self.ROWS - y_grid_name * self.LED_SPACING    ) -   x*2  -2  #) +1 # FIXME
     # only a workin   y = (self.ROWS - y_grid_name * self.LED_SPACING    ) -   x*2  -1  #) +1 # FIXME 
        y = (self.ROWS - y_grid_name * self.LED_SPACING    ) -   x*2  -1  #) +1 # FIXME 

        print (x, y)
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

        #self.layout.set( 0, COLORS.red)
        #self.layout.set( 3, COLORS.yellow)
        #self.layout.set( 6, COLORS.blue)
        #self.layout.set( (18-1)*3, COLORS.blue)


        #self.layout.set(0, 0, COLORS.red)
        #self.layout.set(0, 1, COLORS.yellow)
        #self.layout.set(0, 2, COLORS.blue)
        #self.layout.set(1, 0, COLORS.red)
        #self.layout.set(1, 1, COLORS.yellow)
        #self.layout.set(1, 2, COLORS.blue)
        #self.layout.push_to_driver()

        #time.sleep(10)


        #print ("A1")
        #self.set_hold ("A1", COLORS.red)
        #self.layout.push_to_driver()
        #time.sleep(1)

        self.layout.set(self.MAPPING["A1"], COLORS.blue)
        self.layout.set(self.MAPPING["K1"], COLORS.blue)
        self.layout.set(self.MAPPING["B1"], COLORS.blue)
        self.layout.set(self.MAPPING["F1"], COLORS.blue)
        self.layout.push_to_driver()
        time.sleep (5)

        for j in range (9,11+1):
            for i in range(1,18+1): 
                le = chr(j+65)
                h = le+str(i)
                print (h)
                self.layout.set(self.MAPPING[h], COLORS.red)
                #self.set_hold (h, COLORS.red)
                self.layout.push_to_driver()
                time.sleep(0.01)
            time.sleep (0.5)
            self.clear()

        #for i in range(1,18+1): 
        #    h = "B"+str(i)
        #    print (h)
        #    self.set_hold (h, COLORS.yellow)
        #    self.layout.push_to_driver()
        #    time.sleep(0.01)

      
        #time.sleep(20)

        #self.set_hold ("K17", COLORS.green)
        #self.set_hold ("K18", COLORS.green)
        
        #self.layout.push_to_driver()
                
        #time.sleep(10)
        

        #with open('../problems/HoldSetup.json') as json_file: # FIXME: path 
        #    data = json.load(json_file)
        #    for hold in data[self.SETUP]:
        #        holdset = (data[self.SETUP][hold]['HoldSet']) # A, B, OS for 2016 
        #        color = COLORS.yellow
        #        if (holdset == "A"): # FIXME
        #            color = COLORS.red
         #       if (holdset == "B"):# FIXME
         #           color = COLORS.blue
         #       if (holdset == "OS"):# FIXME
         #           color = COLORS.yellow
#
         #       self.set_hold (hold, color)
         #       self.layout.push_to_driver()
                #print "Orientation"

         #       time.sleep(duration)

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
    parser.add_argument('--special_gz_layout',  action='store_true')
    args = parser.parse_args()
        
    print("Test MOONBOARD LEDS\n===========")
    led_layout = LED_LAYOUT['gz'] if args.special_gz_layout else None
    MOONBOARD = MoonBoard(args.driver_type,led_layout )
    print("Run animation,")
    #animation=
    MOONBOARD.run_animation()
    #MOONBOARD.layout.fillScreen(COLORS.red)
    print(f"wait {args.duration} seconds,")
    time.sleep(args.duration)
    print("clear and exit.")
    MOONBOARD.clear()