# -*- coding: utf-8 -*-
import problems
from server import main 
import argparse
import asyncio
from led.moonboard import MoonBoard,LED_LAYOUT
###############
###############
# GLOBALS
#paths
if __name__ == "__main__":

    import logging
    import sys

    parser = argparse.ArgumentParser(description='Chair Service.')
    parser.add_argument('setup', choices=problems.SETUPS)
    for hs in problems.HOLDS_SETS:
        parser.add_argument(f'-{hs}', action="store_true")
    parser.add_argument('--driver_type', type=str,
                        help='driver type, depends on leds and device controlling the led.',
                        choices=['PiWS281x', 'WS2801', 'SimPixel'],
                        default='WS2801')

    parser.add_argument('--brightness',  default=100, type=int)

    parser.add_argument('--duration',  type=int, default=10,
                        help='Delay of progress.')
    parser.add_argument('--special_nest_layout',  action='store_true')
    parser.add_argument('--debug',  action = "store_true")


    args = parser.parse_args()
    argsd=vars(args)
    logger = logging.getLogger('websockets.server')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    hold_sets = {k for k in problems.HOLDS_SETS if argsd[k]}
    #problems

    led_layout = LED_LAYOUT['nest'] if args.special_nest_layout else None
    MOONBOARD = MoonBoard(args.driver_type,led_layout)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(logger, MOONBOARD, args.setup, hold_sets))
    asyncio.get_event_loop().run_forever()
