from app.modules import *
from app.push_s3 import push_s3
from app.update_status_db import update_status
from logger import *
import logging
import json
from pathlib import Path
import shutil
from app.kibana_logs import print_log

app = FastAPI(docs_url=None, redoc_url=None)

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
#app = FastAPI()
#app = FastAPI(swagger_ui_parameters={"deepLinking": False})


# today=datetime.now()
# date_time = today.strftime("%m-%d-%Y-%H-%M-%S-%f")


# folder_name =str(date_time)
# print("folder name ==", folder_name)

class InvalidDataException(HTTPException):
    def __init__(self, model_name: str):
        self.model_name = model_name
        super().__init__(status_code=422, detail=f"Invalid data for model {model_name}")

def execute_commands_pre(data, vendor, cnf_type):
      today=datetime.now()
      date_time = today.strftime("%m-%d-%Y-%H-%M-%S-%f")
      folder_name =str(date_time)
      print("folder name ==", folder_name)
      operation=data["operation"]
      request_id=data["request_id"]
      logfile = "precheck-"+vendor+"-"+cnf_type+"-"+date_time+".txt"
      path="/tmp/"+str(request_id)+"_output"
      directory_path = Path(path)  # Specify the desired directory path
    # Create a directory
      directory_path.mkdir(parents=True, exist_ok=True)
      #data=data.json()
      #data=json.loads(data)
      print(data)

      level_info = "INFO"
      level_error = "ERROR"

      print("--------------")
      print(request_id)
      #s3_role=data["s3_role"]
      #s3_bucket=data["s3_bucket"]
      #s3_input_dir=data["s3_input_dir"]

      kubectllist=[]
      nf_list=[]
      for i in range(0, len(data["commands"])):
            kubectllist=[]
            nf_list=[]
            status=''
            print("******************************************************************************************")
            for key, value in data["commands"][i].items():
                 if key == "kubectl_commands":
                     for j in range(0, len(data["commands"][i][key])):
                        kubectllist.append(data["commands"][i][key][j])
                 elif key == "nf_commands":
                     for p in range(0, len(data["commands"][i][key])):
                        nf_list.append(data["commands"][i][key][p])
            print(f'final kubectl list is {kubectllist}')
            print_log(request_id,f'Prechecks --> Kubectl commands list to be executed are : {kubectllist}',level_info)
            print(f'final nfctl list is {nf_list}')
            print_log(request_id,f'Prechecks --> nfctl commands list to be executed are : {nf_list}',level_info)
            if cnf_type == "upfd":
                    status=execute_commands_upfd(kubectllist, nf_list, data, logfile)
            elif cnf_type == "amf":
                    status=execute_commands_amf(kubectllist, nf_list, data,logfile)
            elif cnf_type =="smf":
                    status=execute_commands_smf(kubectllist, nf_list, data,logfile)

      
      print("now pushing to s3")
      result_push=push_s3(data, folder_name, logfile)
      print("++++++")
      print(result_push)
      if os.path.exists(path):
          shutil.rmtree(path)
      if result_push == "Failure" and status == "Failure":
        data={
                "request_id":request_id,
                "s3_dir": '',
                "request_status": status,
                "desc": ""
            
            }
        update_status(data)
        return True
      elif result_push !="Failure" and status=="Failure":
         print("insside s3 sucess")
         print(result_push)
         data={
                      "request_id":request_id,
                        "s3_dir": data["s3_data"]["s3_input_dir"]+"/"+folder_name,
                        "request_status": status,
                        "desc": "NF command execution failed"
                 }
         update_status(data)
         return True
      elif result_push =="Failure" and status!="Failure":
         print("insside s3 sucess")
         print(result_push)
         data={
                      "request_id":request_id,
                        "s3_dir": data["s3_data"]["s3_input_dir"]+"/"+folder_name,
                        "request_status": result_push,
                        "desc": "S3 push failed"
                 }
         update_status(data)
         return True        
      else:
         print("insside s3 sucess")
         print(result_push)
         data={
                      "request_id":request_id,
                        "s3_dir": data["s3_data"]["s3_input_dir"]+"/"+folder_name,
                        "request_status": status,
                        "desc": status
                 }
         update_status(data)
         return True
      
 


def execute_commands_post(data,vendor, cnf_type):
      print("Now i am doing post check validation")
      today=datetime.now()
      date_time = today.strftime("%m-%d-%Y-%H-%M-%S-%f")
      folder_name =str(date_time)
      print("folder name ==", folder_name)
      request_id=data["request_id"]      
      logfile = "postcheck-"+vendor+"-"+cnf_type+"-"+date_time+".txt"
      path="/tmp/"+str(request_id)+"_output"
      directory_path = Path(path)  # Specify the desired directory path
    # Create a directory
      directory_path.mkdir(parents=True, exist_ok=True)
      #data=data.json()
      #data=json.loads(data)
      print(data)
      site_bucket_tar=data["site_bucket_tar"]
      request_id=data["request_id"]
      operation=data["operation"]

      level_info = "INFO"
      level_error = "ERROR"

      for i in range(0, len(data["commands"])):
            kubectllist=[]
            nf_list=[]
            for key, value in data["commands"][i].items():
                 if key == "kubectl_commands":
                     for j in range(0, len(data["commands"][i][key])):
                        kubectllist.append(data["commands"][i][key][j])
                 elif key == "nf_commands":
                     for p in range(0, len(data["commands"][i][key])):
                        nf_list.append(data["commands"][i][key][p])
            print(f'final kubectl list is {kubectllist}')
            print_log(request_id,f'Postchecks --> Kubectl commands list to be executed are : {kubectllist}',level_info)
            print(f'final nfctl list is {nf_list}')
            print_log(request_id,f'Postchecks --> nfctl commands list to be executed are  : {nf_list}',level_info)
            if cnf_type == "upfd":
                    print("inside postcheck upfd")
                    download_file(site_bucket_tar,str(request_id))
                    execute_commands_post_upfd(kubectllist, nf_list, data,logfile)
                    status=download_s3(data)
                    # if status=="Failure":
                    #     data={
                    #             "request_id":request_id,
                    #             "s3_dir": '',
                    #             "request_status": status,
                    #             "desc": status
                            
                    #         }
                    #     update_status(data)
                    # file1='/tmp/'+str(request_id)+'_output/precheck_admin_save.cfg'
                    # file2='/tmp/'+str(request_id)+'_output/postcheck_admin_save.cfg'
                    # outputfile='/tmp/'+str(request_id)+'_output/diff_prepost_admin_save.cfg'
                    # grenreate_diff(file1,file2,outputfile)
                    #push_s3(data,folder_name,logfile_post)
            elif cnf_type == "amf":
                    print("inside postcheck amf")
                    execute_commands_amf_post(kubectllist, nf_list, data,logfile)
                    status=download_s3(data)
                    if status=="false":
                        status="Success"
                    # if status=="Failure":
                    #     data={
                    #             "request_id":request_id,
                    #             "s3_dir": '',
                    #             "request_status": status,
                    #             "desc": status
                            
                    #         }
                    #     update_status(data)
                    # file1='/tmp/'+str(request_id)+'_output/precheck_admin_save.cfg'
                    # file2='/tmp/'+str(request_id)+'_output/postcheck_admin_save.cfg'
                    # outputfile='/tmp/'+str(request_id)+'_output/diff_prepost_admin_save.cfg'
                    # grenreate_diff(file1,file2,outputfile)
            elif cnf_type =="smf":
                print("inside postcheck smf")                
                download_file(site_bucket_tar,str(request_id))
                execute_commands_smf_post(kubectllist, nf_list, data,logfile)
                status=download_s3(data)
                # if status=="Failure":
                #     data={
                #             "request_id":request_id,
                #             "s3_dir": '',
                #             "request_status": status,
                #             "desc": status
                        
                #         }
                #     update_status(data)
      if cnf_type != "amf":    
          file1='/tmp/'+str(request_id)+'_output/precheck_admin_save.cfg'
          file2='/tmp/'+str(request_id)+'_output/postcheck_admin_save.cfg'
          outputfile='/tmp/'+str(request_id)+'_output/diff_prepost_admin_save.cfg'
          if status=="Success":
             grenreate_diff(file2,file1,outputfile)
      print("******************************************************************************************")
      print("now pushing to s3")
      result_push= push_s3(data, folder_name, logfile)
      print("++++++")
      print(result_push)
      if os.path.exists(path):
          shutil.rmtree(path)
      if os.path.exists("/tmp/"+str(request_id)):
          shutil.rmtree("/tmp/"+str(request_id))      
      if result_push == "Failure" and status == "Failure":
        data={
                "request_id":request_id,
                "s3_dir": '',
                "request_status": status,
                "desc": ""
            
            }
        update_status(data)
        return True
      elif result_push !="Failure" and status=="Failure":
         print("insside s3 sucess")
         print(result_push)
         data={
                      "request_id":request_id,
                        "s3_dir": data["s3_data"]["s3_input_dir"]+"/"+folder_name,
                        "request_status": status,
                        "desc": "NF command execution failed"
                 }
         update_status(data)
         return True
      elif result_push =="Failure" and status!="Failure":
         print("insside s3 sucess")
         print(result_push)
         data={
                      "request_id":request_id,
                        "s3_dir": data["s3_data"]["s3_input_dir"]+"/"+folder_name,
                        "request_status": result_push,
                        "desc": "S3 push failed"
                 }
         update_status(data)
         return True        
      else:
         print("insside s3 sucess")
         print(result_push)
         data={
                      "request_id":request_id,
                        "s3_dir": data["s3_data"]["s3_input_dir"]+"/"+folder_name,
                        "request_status": status,
                        "desc": status
                 }
         update_status(data)
         return True

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

#@app.post("/podinfo/", response_model=podinforesponse)
@app.post("/fetch/podinfo/{vendor}/{cnf_type}")
async def read_item(req: podinfo,vendor:str, cnf_type:str):


     #print(f"vendor is {vendor}")
     #print(f"cnf type is {cnf_type}")

     #{'@timestamp':'','@version':'1','message':'','external_request_id': order_id,'level':'INFO'}
     #print(f"{'@timestamp': '{datetime.now}', '@version': '1', 'message': 'Request ID received  is - ' {req.request_id}, 'external_request_id':{req.request_id} : 'level' : 'INFO' } \n")
     #logger.info("received message")
     #logger_cluster.debug('Quick zephyrs blow, vexing daft Jim.')
     print(f"{datetime.now()}, {req.request_id}: request id is  \n")
     print(f"{req.request_id}:Incoming request received is {req}")
     print(f"cnf_namespace is {req.cnf_namespace} \n")
     print(f"eks_cluster_kube_config is {req.eks_cluster_kube_config} \n")
     print(f"eks_cluster_name is {req.eks_cluster_name} \n")
     print(f"target_cluster_role is {req.target_cluster_role} \n")
     print(f"cred {req.creds} \n")
     print(f"interface {req.interface} \n")


     if cnf_type == "upfd":
       result=get_pod_info_upfd(req)
     elif cnf_type== "amf":
        result=get_pod_info_amf(req)
     elif cnf_type=="smf":
        result=get_pod_info_smf(req)
     #print("Length of return value ==", len(result))
     print(result)
     return result


#      return {
#         "pod_name":podname,
#         "oam_ip": pod_ip,
#         "oam_port": "2222",
#         "cmd_prompt": prompt,
#         "S5S8-Loopback": ip
# }
  

@app.post("/precheck/{vendor}/{cnf_type}")
async def show_commands(vendor:str, cnf_type:str, background_tasks: BackgroundTasks, inreq: commandsinfo):
      #service= service.lower()

      if not inreq.deploy_env:
             print("*****")
             raise InvalidDataException("Item")
             return {"missing field": inreq}


      try:
        inreq = inreq.dict()
      except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
      

      #print(f"Service received is {service}")
      #if service == "precheck":
      background_tasks.add_task(execute_commands_pre, inreq, vendor, cnf_type)

      return {"message": "Completed"}
@app.post("/postcheck/{vendor}/{cnf_type}")
async def show_commands(vendor:str, cnf_type:str,  background_tasks: BackgroundTasks, inreq: commandsinfos):
      #service= service.lower()

      if not inreq.deploy_env:
             print("*****")
             raise InvalidDataException("Item")
             return {"missing field": inreq}


      try:
        inreq = inreq.dict()
      except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
      


      background_tasks.add_task(execute_commands_post, inreq, vendor, cnf_type)

      return {"message": "Completed"}
