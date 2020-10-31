#!/usr/bin/python
ROWS = 18
COLS = 11
LED_SPACING = 1#3

# Every Col Bottom>Up Left>Right
print ("Layout 1")
led_number = 0
layout = [[0 for i in range(COLS)] for j in range(ROWS)]  
for c in range (0,COLS):
    for r in range(0,ROWS):
        layout[ROWS-1-r][c] = led_number
        led_number = led_number+LED_SPACING
print(layout) 

# Every Row Left>Right Bottom>Up
print ("Layout 2")
led_number = 0
layout = [[0 for i in range(COLS)] for j in range(ROWS)]  
for r in range(0,ROWS):
    for c in range (0,COLS):
        layout[ROWS-1-r][c] = led_number
        led_number = led_number+LED_SPACING
print(layout) 

# ZigZag: Left,Bottom>Left,Up >> 1 Right&Up>Down   -- aka: Evo
print ("Layout 3")
led_number = 0
layout = [[0 for i in range(COLS)] for j in range(ROWS)]  
for c in range (0,COLS):
    for r in range(0,ROWS):
        if (c %2) == 0:
            layout[ROWS-1-r][c] = led_number
        else:
            layout[r][c] = led_number
        led_number = led_number+LED_SPACING
print(layout) 