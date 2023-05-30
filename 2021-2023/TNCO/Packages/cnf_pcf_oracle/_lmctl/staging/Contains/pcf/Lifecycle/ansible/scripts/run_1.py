import sys
import json
import json
# Opening JSON file
f = open(sys.argv[8],)
# returns JSON object as 
# a dictionary
#print(type(f))
try:
  data = json.load(f)
except:
  data=json.dumps(f)

#print(len(data["exportData"]))
name_table=[]
for i in  range(0,len(data["exportData"])):
  name_table.append(data["exportData"][i]["name"])

#print(name_table)
index_default=name_table.index("DefaultPCCRule")
exportData=data["exportData"]
defaultPCCRuleTable=exportData[index_default]["rows"]

#print(sliceDetailsTable)
default_rownumber=[]
slice_rownumber=[]
for rows in defaultPCCRuleTable:
  default_rownumber.append(rows["RowNumber"])
#print(max(default_rownumber))
sliceName=sys.argv[1]+'-'+sys.argv[2]
defaultData={'SubsPlanMappingId': '*', 'SliceName': sliceName, 'RowNumber': max(default_rownumber)+1, 'SessionRuleName': [sys.argv[5]], 'DNN': sys.argv[3], 'PCCRuleName': [sys.argv[6]]}

defaultPCCRuleTable.append(defaultData)

exportData[index_default]["rows"]=defaultPCCRuleTable
data["exportData"]=exportData



#print("******")
with open(sys.argv[8], 'w') as convert_file:
     convert_file.write(json.dumps(data,indent=2,separators=(',', ': ')))
print(type(data))
