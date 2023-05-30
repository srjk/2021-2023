import sys
import json
import json
  
# Opening JSON file
f = open('/tmp/test_file.json',)
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
index_default=name_table.index("DefaultPCCRuleTable")
index_slice=name_table.index("SliceDetailsTable")
exportData=data["exportData"]
defaultPCCRuleTable=exportData[index_default]["rows"]
sliceDetailsTable=exportData[index_slice]["rows"]

#print(sliceDetailsTable)
default_rownumber=[]
slice_rownumber=[]
for rows in defaultPCCRuleTable:
  default_rownumber.append(rows["RowNumber"])
for rows in sliceDetailsTable:
  slice_rownumber.append(rows["RowNumber"])
#print(max(default_rownumber))
sliceName=sys.argv[1]+'-'+sys.argv[2]
defaultData={'RoamingType': '*', 'SliceName': sliceName, 'RowNumber': max(default_rownumber)+1, 'SessionRule': sys.argv[5], 'Rate-plans': sys.argv[4], 'dnn': sys.argv[3], 'PccRuleList': [sys.argv[5]]}
sliceData={'SD': sys.argv[2], 'SST': sys.argv[1], 'SliceName': sliceName, 'RowNumber': max(slice_rownumber)+1 }

defaultPCCRuleTable.append(defaultData)
i=0
for rows in sliceDetailsTable:
  if (rows["SD"]==sys.argv[2] and rows["SST"]==sys.argv[1]):
    i=1
    break

if(i==0):
  sliceDetailsTable.append(sliceData)

exportData[index_default]["rows"]=defaultPCCRuleTable
exportData[index_slice]["rows"]=sliceDetailsTable
data["exportData"]=exportData



#print("******")
with open('/tmp/test_file.json', 'w') as convert_file:
     convert_file.write(json.dumps(data,indent=2,separators=(',', ': ')))
print(type(data))
