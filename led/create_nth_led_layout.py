#!/usr/bin/python
# This script is used to create the arrays for the LED layouts
ROWS = 18
COLS = 11
LED_SPACING = 3

# Every Col Bottom>Up Left>Right
print ("Layout 1 - Col")
led_number = 0
layout = [[0 for i in range(COLS)] for j in range(ROWS)]  
for c in range (0, COLS):
    for r in range(0, ROWS):
        layout[ROWS-1-r][c] = led_number
        led_number = led_number + LED_SPACING
print(layout) 

# Every Row Left>Right Bottom>Up
print ("Layout 2 - Row")
led_number = 0
layout = [[0 for i in range(COLS)] for j in range(ROWS)]  
for r in range(0, ROWS):
    for c in range (0, COLS):
        layout[ROWS-1-r][c] = led_number
        led_number = led_number + LED_SPACING
print(layout) 

# ZigZag: Left,Bottom>Left,Up >> 1 Right&Up>Down   -- aka: Evo
print ("Layout 3 - ZigZag")
led_number = 0
layout = [[0 for i in range(COLS)] for j in range(ROWS)]  
for c in range (0, COLS):
    for r in range(0, ROWS):
        if (c %2) == 0:
            layout[ROWS-1-r][c] = led_number
        else:
            layout[r][c] = led_number
        led_number = led_number + LED_SPACING
print(layout)

# Hold Layout
print ("Layout Holds")
layout = [[0 for i in range(COLS)] for j in range(ROWS)]  
for c in range (0, COLS):
    for r in range(0, ROWS):
        hold = (chr(c+65)+str(r+1))
        layout[ROWS-1-r][c] = hold
print (layout)


# List of all holds
print ("List of all holds")
layout = [0 for i in range(COLS*ROWS)]
for c in range (0, COLS):
    for r in range(0, ROWS):
        hold = (chr(c+65)+str(r+1))
        layout[c*ROWS+r] = hold 
print (layout)
