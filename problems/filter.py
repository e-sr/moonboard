#!/usr/bin/python
import json

SETUP="2016"
with open('problems/HoldSetup.json') as json_file:
    data = json.load(json_file)
    for hold in data[SETUP]:
        holdset = (data[SETUP][hold]['HoldSet']) # A, B, OS for 2016 
        #print (holdset)

print ("Jajajaja")
with open('problems/holds_tmp/holds_moonboard2016.tmp') as json_file:
    data = json.load(json_file)
    #for a in data["Data"]:
        #b = (data["Data"][a])
        #print (b)
    for hs in range (0,len(data["Data"])-1):
        for id in data["Data"][hs]:
            #print (id)
            if (id == "Description"):
                holdset = data["Data"][hs][id]
            #print (data["Data"][0][id])
            if (id == "Holds"):
                #print (data["Data"][0][id][0])
                for hh in data["Data"][hs][id]:
                    #print (hh)
                    #print (hh["Location"])
                    holdname = (hh["Location"]["Description"])
                    holddirection = (hh["Location"]["DirectionString"])
                    holdnumber = (hh["Location"]["HoldNumber"])
                    print (holdname, holddirection, holdnumber, holdset)
                    #


        #for hhh in data["Data"][0][id]["Holds"]:
        #    print (hhh)
    #print (data["Data"][0])