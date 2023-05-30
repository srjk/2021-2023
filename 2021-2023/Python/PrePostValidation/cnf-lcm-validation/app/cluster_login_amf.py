import time
from tempfile import TemporaryDirectory
from datetime import datetime
from datetime import date
import os
import pexpect
import subprocess
import shlex
import boto3
import yaml
import substring
import re
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import logging
import sys
#from app.logger import init_logging
from app.kibana_logs import print_log

def get_pod_info_amf(data):

    level_info = "INFO"
    level_error = "ERROR"
    request_id=data.request_id
    role_arn=data.target_cluster_role
    cluster_name=data.eks_cluster_name
    namespace=data.cnf_namespace
    kubeconfigupdate=data.eks_cluster_kube_config
    
    """
    role_arn="arn:aws:iam::268785957902:role/na4d-s3bucket-execution"
    cluster_name="nk-rdc-eks-cluster-dev-nk-rdc-ibm-e1dev"
    namespace="useast1amf01"
    kubeconfigupdate="aws eks update-kubeconfig --name nk-rdc-eks-cluster-dev-nk-rdc-ibm-e1dev --region us-east-1 --role-arn arn:aws:iam::268785957902:role/nk-rdc-AuthMaster-dev-us-east-1-nk-rdc-ibm-e1dev"
    """
    #Creacting STS boto session to assume role
    try:
        sts = boto3.client("sts")
        assumed = sts.assume_role(RoleArn=role_arn,RoleSessionName="mysession", DurationSeconds=900)

    except Exception as e:
        print(e)
        sys.exit()

    #print(f'{datetime.now()}  : "Assumed Credentials are {assumed}')
    #print(f'{datetime.now()}  : "Role to assume is {role_arn}')
    #logging.info("%s Assumed credentials are \n", {assumed})
    logging.info("Role to assume are %s\n", role_arn)
    print('##################################')
    print_log(request_id,role_arn,level_info)



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
        command=kubeconfigupdate
        cmd_split = shlex.split(command)
        print(cmd_split)
        subprocess.run(cmd_split)
    except Exception as e:
         print("Got Exception while executing Update kube config", e)
         return e

    time.sleep(10)
    podname=''
    config.load_kube_config()
    try:
                c = Configuration().get_default_copy()
    except AttributeError:
                c = Configuration()
                c.assert_hostname = False
    Configuration.set_default(c)
    core_v1 = core_v1_api.CoreV1Api()
    pod_list=core_v1.list_namespaced_pod(namespace)


    try:
        print("inside pod list")
        pod_list=core_v1.list_namespaced_pod(namespace)
        #print_log(request_id,pod_list,level_info)
        #print(pod_list)
        if not pod_list.items:
            print("got length as zero")
            return "Pod list appears to be empty. Check name space"
            sys.exit()
    except Exception as e:
         print("Pod list appears to be empty. Check name space", e)
         print_log(request_id,e,level_error)
         return e
         sys.exit()



    try:
        p=subprocess.run("kubectl get ns", shell=True,capture_output=True, text=True,timeout=20)
        if p.returncode == 0:
            print(p.stdout)
        else:
            print("Error: ",p.stderr)
    except Exception as e:
         print("Unable to execute kubectl commands", e)
         return e
         sys.exit()
    print("************************************************************************************************************************************")

    if cluster_name =="ibm-dev" or cluster_name == "dish-sandbox":
        try:
            for pod in pod_list.items:
                pod_name=pod.metadata.name
                print(f'{datetime.now()}  : Following pods Exist {pod_name}')
                if "loam-a" in pod_name:
                    podname=pod_name
                print(f'{datetime.now()} following pods exist, {podname}')
                print_log(request_id,podname,level_info)
        except ValueError as esc:
            print(f'{datetime.now()}  : No ALD pods exist')
            sys.exit(2)
        print(f'{datetime.now()} following pods exist, {podname}')
        print_log(request_id,podname,level_info)


        p=subprocess.run("kubectl get pod -o wide -n "+namespace+" | grep loam-a | awk '{print $6}'",shell=True,capture_output=True, text=True)
        #print(p)
        #p=p.decode("utf-8")
        podip=p.stdout.replace('\n','')
        #out=str(p.communicate())
        #print("#####################", out)
        #return podip,podname,podname,"172.31.253.4"
      
        data={
                "pod_name_active": podname,
               "pod_name_standby": "",
                "oam_ip": podip,
                "oam_port": "2222",
                "S5S8-Loopback":  "",
                "flash_name": "",
                "cmd_prompt":podname
         }
        print("data is", data)
        print_log(request_id,data,level_info)
        return data



    try:
          for pod in pod_list.items:
             pod_name=pod.metadata.name
             #print(f'{datetime.now()}  : Following pods Exist {pod_name}')
             if "necc" in pod_name:
                podname=pod_name
                try:
                    output="test"
                    result=subprocess.run("kubectl exec -it "+podname+" -n "+namespace+"  -- ip -all address|grep secondary", shell=True,capture_output=True, text=True,timeout=20)
                    # output = result.stdout
                    # error = result.stderr
                    print(result.returncode)
                    if result.returncode == 0:
                        # Subprocess ran successfully
                        #print("output"+result.stdout)
                        output = result.stdout
                        #print(output)
                        print_log(request_id,output,level_info)
                        # Process the output as needed
                    else:
                        # Error occurred
                        error = result.stderr
                        # Process the error message or take appropriate action
                        print("Error:", error)
                        print_log(request_id,error,level_error)
            # Get the return code of the subprocess
                    return_code = result.returncode
                    print("++++")
                    if output=="test":
                        continue

                    #print(output)
                    ip_address = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', output)
                    if ip_address:
                        podip = ip_address.group()
                        print(podip)
                        print_log(request_id,podip,level_info)
                        break
                    else:
                      print("No IP address found.")
                except Exception as e:
                    print("Unable to get Active address", e)
                    return e
             #print(f'{datetime.now()} following pods exist, {podname}')
    except ValueError as esc:
          print(f'{datetime.now()}  :  pod dosnt exist')
          sys.exit(2)
    print(f'{datetime.now()} following pods exist, {podname}')
    print_log(request_id,podname,level_info)



    # p=subprocess.Popen("kubectl exec -it "+podname+ " -n "+ namespace+" -- ip -all address | grep secondary |awk '{print $2}'", stdout=subprocess.PIPE, shell=True)
    # #print(p)
    # p.wait()
    # if p.returncode != 0:
    #   print("Error:", p.stderr.read().decode())    
    # out=str(p.communicate())
    # #print("#####################", out)
    # out=out.replace('(', '').replace(')', '').strip('None').replace(',', '').replace("'", "")
    # s = substring.substringByChar(out, startChar="b", endChar="/")
    # podip = s.replace('/', "").replace('b','')
    # print(f"The final pod ip is {podip} {podname}")
    # # return {podip, podname}
    data={
                "pod_name_active":podname,
               "pod_name_standby":"",
                "oam_ip": podip,
                "oam_port": "22",
                "cmd_prompt": podname,
                "S5S8-Loopback": "",
                "flash_name": "cf1-a"
         }
    print("data is", data)
    print_log(request_id,data,level_info)
    return data