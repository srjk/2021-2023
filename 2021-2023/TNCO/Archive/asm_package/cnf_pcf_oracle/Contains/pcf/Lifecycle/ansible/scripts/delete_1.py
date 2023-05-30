import sys
import json
import json
  
# Opening JSON file
f = open('/tmp/test_file.json',)
  
# returns JSON object as 
# a dictionary
try:
  data = json.load(f)
except:
  data=json.dumps(f)

temp_data= data["exportData"][0]["rows"]
    
for x in range(0,len(temp_data)):
  i= x
  x= data["exportData"][0]["rows"][x]
  if x["SST"] == sys.argv[1] and x["SD"] == sys.argv[2] and x["dnn"] == sys.argv[3] and x["Rate-plans"]== sys.argv[4]:
    try:
      x["PccRuleList"].remove(sys.argv[6])
    except:
      x["PccRuleList"]=x["PccRuleList"]
    if len(x["PccRuleList"])== 0:
      data["exportData"][0]["rows"].remove(x)
    break

with open('/tmp/test_file.json', 'w') as convert_file:
     convert_file.write(json.dumps(data))
print(data)

