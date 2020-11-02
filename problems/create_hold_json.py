#!/usr/bin/python
# Convert JSON hold setups (extracted from moonboard.com) to readable JSON for this script set
import json

outfile="HoldSetup.txt"

ff = {}

for layout in ["Moonboard2016", "MoonboardMasters2017", "MoonboardMasters2019", "Minimoonboard2020"]:
    with open('problems/holds_tmp/'+layout+'.tmp') as json_file:
        dd = {}
        data = json.load(json_file)
        for hs in range (0,len(data["Data"])-1):
            for id in data["Data"][hs]:
                if (id == "Description"):
                    holdset = data["Data"][hs][id]
                if (id == "Holds"):
                    for hh in data["Data"][hs][id]:
                        holdname = (hh["Location"]["Description"])
                        holddirection = (hh["Location"]["DirectionString"])
                        holdnumber = (hh["Location"]["HoldNumber"])
                        ee = {}
                        ee["Orientation"] = holddirection
                        ee["HoldSet"] = holdset
                        ee["Hold"] = holdnumber
                        dd[holdname] = ee

                        #print (layout, holdname, holddirection, holdnumber, holdset)    
        ff[layout] = dd

with open(outfile, 'w') as f:
  json.dump(ff, f, ensure_ascii=False)    