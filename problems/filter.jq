#.Data[] | {HH: .Holds[].Location.Description, Ori: .Holds[].Location.DirectionString, Num: .Holds[].Location.HoldNumber} 


#cat holds_moonboard2016|jq ".Data[] | (.Description)"|head -n40 
#cat holds_moonboard2016|jq ".Data[] | (.Holds[]) | (.Location.Description, .Location.DirectionString, .Location.HoldNumber)" |head -n40
#cat holds_moonboard2016|jq ".Data[] | {Holdset: .Description, HH: .Holds[].Location.Description, Ori: .Holds[].Location.DirectionString, Num: .Holds[].Location.HoldNumber} "|head -n40                
#cat holds_moonboard2016|jq ".Data[] | (.Description {Holdset: .Description, HH: .Holds[].Location.Description, Ori: .Holds[].Location.DirectionString, Num: .Holds[].Location.HoldNumber}) "|head -n40
.Data[] | {(.Holds[].Location.Description): { Holdset: .Description, Orientation: .Holds[].Location.DirectionString, Number: .Holds[].Location.HoldNumber} } 
