import yaml
import json
import sys

list1 = parsed_yaml_file = yaml.load(open(sys.argv[1],'r'), Loader=yaml.FullLoader)

assembly= list1["name"].split('::')
name=assembly[1]
version=assembly[2]
description= list1["description"]
properties= list1["properties"]

href= " "
filename=name+'_'+version+".json"
serviceSpecRelationship= "null"
data= {"name": "",
  "description": "",
  "version": "",  
  "href": " ",   
  "serviceSpecCharacteristic": [],
  "serviceSpecRelationship": "",
  "targetServiceSchema": "DISH",
  "bundle": "" }

data["name"]=name
data["description"]=description
data["bundle"]= False
data["version"]=version
data["serviceSpecRelationship"]=serviceSpecRelationship


serviceSpecCharacteristic=[]
dataArray={
      "name": "",
      "configurable": True,
      "description": "",
      "serviceSpecCharacteristicValue": [
        {
          "isDefault": "false",
	  "valueType": "STRING",
          "value": ""
        }
      ]
    }
checkarray=["type","descrption","default"]
add_value=["SUPI","GPSI"]
remove_array=["deploymentLocation","resourceManager"]
for x in properties:
    dataArray["name"]=x
    if x in remove_array:
       continue
    elif( "value" in properties[x].keys()):
        continue
    elif x in add_value:
        for y in checkarray:
            if ( y in properties[x].keys() ):
                if("description" in properties[x].keys()):
                    dataArray["description"]=properties[x]["description"]
                if("default" in properties[x].keys()):
                    dataArray["serviceSpecCharacteristicValue"][0]["value"]=properties[x]["default"]
                    dataArray["serviceSpecCharacteristicValue"][0]["isDefault"]="true"
                if("type" in properties[x].keys()):
                    dataArray["serviceSpecCharacteristicValue"][0]["valueType"]=properties[x]["type"].upper()
        serviceSpecCharacteristic.append(dataArray)
    elif( "volatile" in properties[x].keys()):
        continue
    else:
        for y in checkarray:
            if ( y in properties[x].keys() ):
                if("description" in properties[x].keys()):
                    dataArray["description"]=properties[x]["description"]
                if("default" in properties[x].keys()):
                    dataArray["serviceSpecCharacteristicValue"][0]["value"]=properties[x]["default"]
                    dataArray["serviceSpecCharacteristicValue"][0]["isDefault"]="true"
                if("type" in properties[x].keys()):
                    dataArray["serviceSpecCharacteristicValue"][0]["valueType"]=properties[x]["type"].upper()
        serviceSpecCharacteristic.append(dataArray)
    dataArray={
    "name": "",
    "configurable": True,
    "description": "",
     "serviceSpecCharacteristicValue": [
     {
        "isDefault": "false",
          "valueType": "STRING",
          "value": ""
        }
      ]
     }



data["serviceSpecCharacteristic"]=serviceSpecCharacteristic
with open(filename,'w') as outfile:
    json.dump(data,outfile,indent=2)
