import sys
import json
import json
  
# Opening JSON file
f = open(sys.argv[7],)
# returns JSON object as 
# a dictionaryi
try:
  data = json.load(f)
except:
  data=json.dumps(f)

name_table=[]
for i in  range(0,len(data["exportData"])):
  name_table.append(data["exportData"][i]["name"])

index_default=name_table.index("DefaultPCCRule")
exportData=data["exportData"]
defaultPCCRuleTable=exportData[index_default]["rows"]
#print(defaultPCCRuleTable)
l=len(defaultPCCRuleTable)
#print(l)
for j in range(l):
 #print("***************************")
 if(defaultPCCRuleTable[j]["SessionRuleName"][0]==sys.argv[5]):
   #print(len(defaultPCCRuleTable))
   del defaultPCCRuleTable[j]
   break

#defaultData={'RoamingType': '*', 'SliceName': '1-0000002', 'RowNumber': max(default_rownumber)+1, 'SessionRule': 'internet-plt-1-000002-sessRule', 'Rate-plans': 'Platinum', 'dnn': 'internet', 'PccRuleList': ['internet-plt-1-000002']}
#sliceData={'SD': '000002', 'SST': '1', 'SliceName': '1-000002', 'RowNumber': max(slice_rownumber)+1 }

#defaultPCCRuleTable.append(defaultData)
#sliceDetailsTable.append(sliceData)

exportData[index_default]["rows"]=defaultPCCRuleTable
data["exportData"]=exportData



#print("******")
with open(sys.argv[7], 'w') as convert_file:
     convert_file.write(json.dumps(data))
print(type(data))
