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
import json
import base64
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import logging
from app.logger import logging


# def listToString(s):
#      # initialize an empty string
#     str1 = ""
#     # traverse in the string
#     for ele in s:
#         str1 += ele
#     # return string
#     return str1


def execute_commands_amf(kubectllist, command_list, data,logfile_pre):

    status = "Success"
    region_value='' #FROM WHERE WILL THE REGION BE READ
    request_id=data["request_id"]
    region_pattern = r"--region\s+(\S+)"
    match = re.search(region_pattern, data["eks_cluster_kube_config"])

    if match:
      region_value = match.group(1)
    # Use the region value in your code
      print("Region:", region_value)
    else:
      print("Region not found in the command string.")
    region_name=region_value
    role_arn=data["target_cluster_role"]
    cluster_name=data["eks_cluster_name"]
    namespace=data["cnf_namespace"]
    kubeconfigupdate=data["eks_cluster_kube_config"]
    cmd_prompt=data["pod_info"]["cmd_prompt"]
    remote_ip = data["pod_info"]["oam_ip"]
    remote_port=data["pod_info"]["oam_port"]
    cred=data["creds"]
    remote_password=json.loads(base64.b64decode(cred).decode('utf-8'))['admin_password']
   # print(f"remote_password = {remote_password}")
    #logger.info(f"remote_password = {remote_password}")
    remote_username = json.loads(base64.b64decode(cred).decode('utf-8'))['admin_user']
    podname=data["pod_info"]["pod_name_active"]


    # print("Inside show commands function")
    # print("kubectl commands are %d ", len(kubectllist))
    # print("command_list is %s ", command_list)

    sts = boto3.client("sts")

    assumed = sts.assume_role(RoleArn=role_arn,RoleSessionName="mysession",DurationSeconds=900)

    print(f'{datetime.now()}  : "Assumed Credentials are {assumed}')
    print(f'{datetime.now()}  : "Role to assume is {role_arn}')


    # these will be different than the ones you started with
    credentials = assumed["Credentials"]
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]

    #setting the env with the creds
    os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
    os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
    os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']


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
    print(f'{datetime.now()}  :  cluster name is  "{cluster_name}')
    if cluster_name not in clusters:
        raise RuntimeError(f"configured cluster: {cluster_name} not found among {clusters}")


    try:
        command=kubeconfigupdate
        cmd_split = shlex.split(command)
        print(cmd_split)
        subprocess.run(cmd_split)
        time.sleep(10)
    except Exception as e:
        status="Failure"
        return status
    request_id=data["request_id"]
    path="/tmp/"+str(request_id)+"_output"
    logfile_pre=path+"/"+logfile_pre    
    print("logfile is +++++++++++++++++++++++++++++++++++++", logfile_pre)
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
            print("hello i am here",p)
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

            child = pexpect.spawn('/bin/bash',['-c',' '.join(exec_command)],encoding='utf-8',timeout=50)
            #child = pexpect.spawn('kubectl -n d1e1dfwupfd01 exec -it loam-a-v1-77dfc56696-4dc56 -- /bin/bash',encoding='utf-8')
            # Expect the SSH password prompt
            #print(child)
            child.delaybeforesend=1
            child.logfile_read = f
            s=child.expect(["#","password"])
            #print(s)
            #print(child.before)
            #print(child.after)
            for r in command_list:
              print("==========")
              print(r)
              if s==1:
                print(remote_password)
                child.sendline(remote_password)
                t=child.expect(["password","#"],timeout=150)
                print(t)
                if t==0:
                    print(remote_password)
                    child.sendline(remote_password)
                    
              #f.write(child.before)
              #print(child.before)
              #iprint(t)
              child.sendline(r)
              #f.write(child.before)
              s=child.expect(["#","password"],timeout=300)
              #print(child.isalive())
            #print('inside')
            child.close(force=True)
            #print(child.isalive())
      try:
        p=subprocess.run('kubectl exec -it -n '+namespace+' '+podname+' -- ls -1t /data-store/backup/ | grep -E ".tar"', shell=True,capture_output=True, text=True,timeout=20)
        if p.returncode == 0:
            print(p.stdout.splitlines())
            filename=p.stdout.splitlines()[0]
            try:
              p=subprocess.run('kubectl cp -n '+namespace+' '+podname+':/data-store/backup/'+filename+' '+filename , shell=True,capture_output=True, text=True,timeout=20,cwd=path)
              if p.returncode == 0:
                  print(p.stdout.splitlines())
                  print(type(p.stdout.splitlines()))
              else:
                  print("Error: ",p.stderr)
            except Exception as e:
              print("Unable to execute kubectl commands", e)
              return e  
        else:
            print("Error: ",p.stderr)
      except Exception as e:
         print("Unable to execute kubectl commands", e)
         return e
      try:
        p=subprocess.run('kubectl cp -n '+namespace+' '+podname+':/data-store/ldap.dat ldap.dat', shell=True,capture_output=True, text=True,timeout=20,cwd=path)
        if p.returncode == 0:
            print(p.stdout.splitlines())
            print(type(p.stdout.splitlines()))
        else:
            print("Error: ",p.stderr)
      except Exception as e:
        print("Unable to execute kubectl commands", e)
        return e  
      try:
        p=subprocess.run('kubectl cp -n '+namespace+' '+podname+':/root/cmmDBdump.log cmmDBdump.log', shell=True,capture_output=True, text=True,timeout=20,cwd=path)
        if p.returncode == 0:
            print(p.stdout.splitlines())
            print(type(p.stdout.splitlines()))
        else:
            print("Error: ",p.stderr)
      except Exception as e:
        print("Unable to execute kubectl commands", e)
        return e      

      f.close()
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