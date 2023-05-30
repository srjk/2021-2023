from pathlib import Path
import re
from tempfile import TemporaryDirectory
import time
from datetime import datetime
from datetime import date
import os
import pexpect
import subprocess
import shlex
import boto3
import yaml
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import logger
import json
import base64
#from app.logger import init_logging
import logging
from app.kibana_logs import print_log

def execute_commands_upfd(kubectllist, command_list, data, logfile_pre):

    level_info = "INFO"
    level_error = "ERROR"

    print("Print inside show commands upfd")
    '''
    logger = logging.getLogger()
    fhandler = logging.FileHandler(filename='std1.log', mode='w', encoding='utf8')
    formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.INFO)
    '''
    status = "Success"
    request_id=data["request_id"]

    #region_name=data["region"] #FROM WHERE WILL THE REGION BE READ

    region_value='' #FROM WHERE WILL THE REGION BE READ

    region_pattern = r"--region\s+(\S+)"
    match = re.search(region_pattern, data["eks_cluster_kube_config"])

    if match:
      region_value = match.group(1)
    # Use the region value in your code
      print("Region:", region_value)
      print_log(request_id,f'Region name is : {region_value}',level_info)
    else:
      print("Region not found in the command string.")
    region_name=region_value

    role_arn=data["target_cluster_role"]
    cluster_name=data["eks_cluster_name"]
    namespace=data["cnf_namespace"]
    kubeconfigupdate=data["eks_cluster_kube_config"]
    remote_ip = data["pod_info"]["oam_ip"]
    remote_port=data["pod_info"]["oam_port"]
    cmd_prompt=data["pod_info"]["cmd_prompt"]
    cred=data["creds"]
    remote_password=json.loads(base64.b64decode(cred).decode('utf-8'))['admin_password']
    #print(f"remote_password = {remote_password}")
    #logger.info(f"remote_password = {remote_password}")
    remote_username = json.loads(base64.b64decode(cred).decode('utf-8'))['admin_user']


    # print("Inside show commands function")
    # print("kubectl commands are %d ", len(kubectllist))
    # print("command_list is %s ", command_list)

    sts = boto3.client("sts")

    try:
        print(f'{datetime.now()}  : "Role to assume is {role_arn}')
        print_log(request_id,f'target_cluster_role is: {role_arn}',level_info)
        assumed = sts.assume_role(RoleArn=role_arn,RoleSessionName="mysession",DurationSeconds=900)

    except Exception as e:
        status = "Failure"
        return status

    # these will be different than the ones you started with
    credentials = assumed["Credentials"]
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]

    #setting the env with the creds
    os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
    os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
    os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']

    try:
        # make sure our cluster actually exists
        eks = boto3.client(
            "eks",
            aws_session_token=session_token,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
        )

        clusters = eks.list_clusters()["clusters"]
        print(f'{datetime.now()}  :  clusters are "{clusters}')
        print_log(request_id,f'List of clusters: {clusters}',level_info) 
        print(f'{datetime.now()}  :  cluster name is  "{cluster_name}')
        print_log(request_id,f'Selected Cluster name is: {cluster_name}',level_info)
        if cluster_name not in clusters:
            raise RuntimeError(f"configured cluster: {cluster_name} not found among {clusters}")
    except Exception as e:
        status="Failure"
        print_log(request_id,"Failure",level_error)
        return status


    try:
        command=kubeconfigupdate
        cmd_split = shlex.split(command)
        print(cmd_split)
        subprocess.run(cmd_split)
    except Exception as e:
        status="Failure"
        return status
    request_id=data["request_id"]
    path="/tmp/"+str(request_id)+"_output"
    logfile_pre=path+"/"+logfile_pre    
    #print("logfile is +++++++++++++++++++++++++++++++++++++", logfile_pre)
    print_log(request_id,f'Final Precheck summary saved under {logfile_pre} and available in S3 for download',level_info)
    f = open(logfile_pre, "a")

 
    try:

      for i in kubectllist:
        exec_command=''
        #print(i)
        #print(type(i))
        f.write(i)
        f.write("\n")
        if not "exec" in i:

            p=subprocess.check_output(i, shell=True,cwd=path)
            p=p.decode("utf-8")
            #out=str(p.communicate())
            #print("hello i am here",p)
            #logger.info(p)
            #logger.info(p)
            #f.write(i+"\n")
            f.write(p)
            f.write("----------------------------------------\n")
        else:
             #print("exec command is", i)
             cmd_split = shlex.split(i)
             #print("command split is ",cmd_split)
             exec_command=cmd_split
             #print("final exec command is", exec_command)
             print_log(request_id,f'Command for login to active pod is :{exec_command}',level_info)

    # Spawn a child process to interact with the SSH session
             child = pexpect.spawn('/bin/bash', ['-c', ' '.join(exec_command)], encoding='utf-8')
             #f.write(exec_command)
             child.logfile_read = f
             child.delaybeforesend=1
             f.write("\n")
             k=child.expect(['password: ',"Are"])
             if k==1:
                 child.sendline("yes")
                 child.expect('password: ')
             child.sendline(remote_password)
             child.expect(cmd_prompt)

             terminal=child.after
             print(f"after terminal is ======================================= {child.after}")
             #    data = ""
             for command in command_list:
               if len(command_list) != 0:
                  print(f'{datetime.now()}  : Command to be executed is  {command}')
                  try:
                      child.sendline(command)
                      #i = child.expect([terminal, 'Press any key to continue', 'Overwrite'], timeout=200)
                      i = child.expect([cmd_prompt, 'Press any key to continue', 'destination file',pexpect.EOF], timeout=300)
                  except Exception as e:
                      status="Failure"
                      print(e)
                      print (i)
                      return status 
                  

                  #print(f"Child before is {child.before}")
                  if i == 0:
                      try:
                          #logger.info(child.before)
                          #logger.info(child.after)
                          #f.write(child.before)
                          f.write("\n")
                          continue
                      except Exception as e:
                          print(e)
                  elif i == 2:
                      #logger.info(child.before)
                      #f.write(child.before)
                      #logger.info(child.before)
                      child.send('y')
                      i=child.expect(cmd_prompt, timeout=300)
                      #print("y ==", i)
                      #logger.info(child.before)
                      #f.write(child.before)
                  elif i == 1:
                      data1=""
                      #print("inside 1")
                      while True:
                          data1 += child.before
                          #logger.info(child.before)
                          #f.write(child.before)
                          child.send('')
                          #child.sendline('y')
                          i=child.expect(['Press any key to continue',cmd_prompt])
                          if i == 1:
                              data1 += child.before
                              data1 += child.after

                              break

                      #print(f"Printing data at the end {data}")
                      #logger.info(data1)
                      #f.write(data1)
                  elif i==3:
                      continue
      f.close()
      child.close(force=True)
      print(child.isalive())  
      #print("********************************************COMPLETED**********************************************************************")
      return status
    except Exception as e:
             print(e)
             status="Failure"
             try:
               f.close()
               child.close(force=True)
               print(child.isalive())
             except:
                f.close()  
             return status

        #child.sendline('logout')