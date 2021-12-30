# -*- coding: utf-8 -*-
import argparse
from led.moonboard import MoonBoard,LED_LAYOUT
from gi.repository import GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from functools import partial
import json 

def new_problem_cb(mb,holds_string):
        holds = json.loads(holds_string)
        mb.show_problem(holds)
        logger.debug('new_problem: '+holds_string)

if __name__ == "__main__":
    import logging
    import sys

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--driver_type',
                        help='driver type, depends on leds and device controlling the led.',
                        choices=["WS281X", 'WS2801', 'SimPixel'],
                        default='WS2801')

    parser.add_argument('--brightness',  default=100, type=int)

    parser.add_argument('--led_layout',  
                        default=None, 
                        choices=list(LED_LAYOUT.keys())
                        )

    parser.add_argument('--debug',  action = "store_true")


    args = parser.parse_args()
    argsd=vars(args)
    logger = logging.getLogger('run')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    #problems
    led_layout = LED_LAYOUT.get(args.led_layout) if args.led_layout is not None else None
    MOONBOARD = MoonBoard(args.driver_type, led_layout)
    MOONBOARD.start_show_leds()
 
    # connect to dbus signal new problem
    dbml = DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    proxy = bus.get_object('com.moonboard','/com/moonboard')

    proxy.connect_to_signal('new_problem', partial(new_problem_cb, MOONBOARD))
    loop = GLib.MainLoop()

    dbus.set_default_main_loop(dbml)

    # Run the loop
    try:
        loop.run()
    except KeyboardInterrupt:
        print("keyboard interrupt received")
    except Exception as e:
        logger.error(str(e))
        print("Unexpected exception occurred: '{}'".format(str(e)))
    finally:
        loop.quit()
