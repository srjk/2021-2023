#Update DB with status requests
import os
import requests
import json
#def update_status():
def update_status(result_final):
    """
    print("final result ==", result_final)
    request_id=result_final["request_id"]
    print("request_id ==", request_id)
    status=result_final["request_status"]
    """

    print(type(result_final))
    result_final["request_id"]=str(result_final["request_id"])   
    #cnf_lcm_url=os.environ['cnf_lcm_url']
    print(result_final)
    host=os.environ.get('LCM_SERVICE')
    cnf_lcm_url=host+"/update/request_status"
    print(cnf_lcm_url)
    headers = {
    'Content-Type': 'application/json'
     }
    response=requests.put(cnf_lcm_url,headers=headers,data=json.dumps(result_final) ,verify=False)

    if response.ok:
        print("Data published successfully")
    else:
        print(f"Error publishing data: {response.status_code} {response.reason}")


#update_status()