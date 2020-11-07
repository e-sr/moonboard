#!/usr/bin/python
# Display a holdset (testing script)
import json
setup='MoonboardMasters2017' 
with open('problems/HoldSetup.json') as json_file:
    data = json.load(json_file)
    for hold in data[setup]:
        holdset = (data[setup][hold]['HoldSet'])
        print (hold, holdset) # A, B, OS
    #    print (d['HoldSet'])
    #    #'HoldSet': 'A'
    #print (data[setup]['D5']["HoldSet"])