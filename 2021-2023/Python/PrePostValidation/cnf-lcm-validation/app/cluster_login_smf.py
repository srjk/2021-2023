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
import json
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import logging
import sys
import paramiko
import base64
import re
#from app.logger import init_logging
from app.kibana_logs import print_log

def get_pod_info_smf(data):

    level_info = "INFO"
    level_error = "ERROR"

    request_id=data.request_id

    role_arn=data.target_cluster_role
    cluster_name=data.eks_cluster_name
    namespace=data.cnf_namespace
    kubeconfigupdate=data.eks_cluster_kube_config
    interface=data.interface
    cred=data.creds
    try:
        password = json.loads(base64.b64decode(cred).decode('utf-8'))['admin_password']
    except Exception as e:
        return e
    try:
        username = json.loads(base64.b64decode(cred).decode('utf-8'))['admin_user']
    except Exception as e:
        return e


    #Creacting STS boto session to assume role
    try:
        #logging.info("Role to assume are %s\n", role_arn)
        #print('##################################')
#        print_log(request_id,role_arn,level_info)
        print_log(request_id,f'target_cluster_role is: {role_arn}',level_info)
        sts = boto3.client("sts")
        assumed = sts.assume_role(RoleArn=role_arn,RoleSessionName="mysession",DurationSeconds=900)

    except Exception as e:
        print(e)
        print("I got an exception while assuming")
        return e
        sys.exit()






    # these will be different than the ones you started with
    credentials = assumed["Credentials"]
    # access_key_id = credentials["AccessKeyId"]
    # secret_access_key = credentials["SecretAccessKey"]
    # session_token = credentials["SessionToken"]

    #setting the env with the creds
    os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
    os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
    os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']

    try:
        command=kubeconfigupdate
        cmd_split = shlex.split(command)
        #print(cmd_split)
        subprocess.run(cmd_split)
    except Exception as e:
         print("Got Exception while executing Update kube config", e)
         return e
         sys.exit()

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

    try:
        print("inside pod list")
        pod_list=core_v1.list_namespaced_pod(namespace)
#        print_log(request_id,pod_list,level_info)
        #print(pod_list)
        if not pod_list.items:
            print("got length as zero")
            print_log(request_id,"got length as zero, Pod list appears to be empty. Check name space",level_error)
            return "Pod list appears to be empty. Check name space"
            sys.exit()
    except Exception as e:
         print("Pod list appears to be empty. Check name space", e)
         print_log(request_id,"Pod list appears to be empty. Check name space",level_error)
         return e
         sys.exit()

    try:
        p=subprocess.run("kubectl get ns", shell=True,capture_output=True, text=True,timeout=20)
        if p.returncode == 0:
            print(p.stdout)
            print_log(request_id,f'List of namespace: {p.stdout}',level_info)
        else:
            print("Error: ",p.stderr)
    except Exception as e:
         print("Unable to execute kubectl commands", e)
         print_log(request_id,"Unable to execute kubectl commands",level_error)
         return e
         sys.exit()


    #print("************************************************************************************************************************************")


    if cluster_name =="ibm-dev" or cluster_name == "dish-sandbox":
        try:
            for pod in pod_list.items:
                pod_name=pod.metadata.name
                print(f'{datetime.now()}  : Following pods Exist {pod_name}')
                if "loam-a" in pod_name:
                    podname=pod_name
                print(f'{datetime.now()} following pods exist, {podname}')
                print_log(request_id,f'Selected podname is : {podname}',level_info)
        except ValueError as esc:
            print(f'{datetime.now()}  : No loam-a pods exist')
            print_log(request_id,"No loam-a pods exist",level_error)
            sys.exit(2)
        print(f'{datetime.now()} following pods exist, {podname}')
        print_log(request_id,f'following pods exist: {podname}',level_info)


        p=subprocess.run("kubectl get pod -o wide -n "+namespace+" | grep loam-a | awk '{print $6}'",shell=True,capture_output=True, text=True)
        #print(p)
        #p=p.decode("utf-8")
        podip=p.stdout.replace('\n','')
        #out=str(p.communicate())
        #print("#####################", out)
        #return podip,podname,podname,"172.31.253.4"

        data={
                "pod_name_active":podname,
                "pod_name_standby":podname,
                "oam_ip": podip,
                "oam_port": "2222",
                "S5S8-Loopback":  "172.31.253.4",
                "flash_name": "cf1-a",
                "cmd_prompt":podname
         }
        print("data is", data)
        print_log(request_id,f'Requested data is : {data}',level_info)
        return data

    try:
          for pod in pod_list.items:
             pod_name=pod.metadata.name
             #print(f'{datetime.now()}  : Following pods Exist {pod_name}')
             if "loam" in pod_name:
                podname=pod_name
                try:
                    output="test"
                    result=subprocess.run("kubectl exec -it "+podname+" -n "+namespace+"  -- ip -all address|grep active", shell=True,capture_output=True, text=True,timeout=20)
                    # output = result.stdout
                    # error = result.stderr
                    print(result.returncode)
                    if result.returncode == 0:
                        output = result.stdout
                        podname_active=podname
                    elif result.returncode == 1:
                        output = result.stdout
                        podname_standby=podname
                    else:
                        # Error occurred
                        error = result.stderr
                        # Process the error message or take appropriate action
                        print("Error:", error)
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
                        #break
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

    if "loam-a" in podname_active:
         flash="cf1-a"
    elif "loam-b" in podname_active:
         flash="cf1-b"
    else:
         flash=""


    ssh_command=f"ssh {username}@{podip} -p 2222"
    print(ssh_command)
    try:
        exec_command = ['kubectl', '-n', namespace, 'exec', '-it',podname_active, '--',ssh_command]
        #exec_command = ['kubectl', '-n', 'd1w2az1smf01', 'exec', '-it','loam-a-v1-9b59485cb-v78qm', '--',' /bin/bash']
        #print(exec_command)
        print_log(request_id,f' Command for login to active pod is : {exec_command}',level_info)
    except Exception as e:
        return e


    #print(f"now spawning the child")
    #for command in command_list:
    # Spawn a child process to interact with the SSH session
    router_command='show router 100 int'
    #print(router_command)
    remote_password=password
    try:
            child = pexpect.spawn('/bin/bash',['-c',' '.join(exec_command)], encoding='utf-8',timeout=20)
            #print_log(request_id,child,level_info)
            #child = pexpect.spawn('kubectl -n d1e1dfwupfd01 exec -it loam-a-v1-77dfc56696-4dc56 -- /bin/bash',encoding='utf-8')
            # Expect the SSH password prompt

            #print(child)
            #print(child.after)
            """
            child.expect('password:')
            print(child.after)
            print("before")
            child.sendline("ssh admin@172.16.128.240 -p 2222\n")
            #print(child.before)
            """
            k=child.expect(['password: ',"Are"],timeout=120)
            if k==1:
                 child.sendline("yes")
                 child.expect('password: ')
            child.sendline(remote_password)
            child.expect("#")
            prompt=child.before.split('\n')
            print(prompt[-1][1:])
            #print(child)
            child.sendline("environment no more")
            child.expect("#")
            child.sendline("show router 100 int")
            child.expect("#",timeout=120)
            #print(child.before)
            output=child.before.split("\n")
            for i,element in enumerate(output):
                if element.find('S5S8-Loopback')!= -1:
                   pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
                   matches=re.findall(pattern,output[i+1])
                   ip_ranges=matches[0]
                   print(ip_ranges)
                   break
            child.sendline("logout")
            #child.expect("#")
            #child.expect(EOF)
            #print(child)
            #print_log(request_id,child,level_info)
            #print('inside')
            child.close(force=True)
            print(child.isalive())
    except Exception as e:
            print(e)
            print_log(request_id,e,level_error)
            return e

    #return podip,podname,prompt,ip_ranges
    data={
                "pod_name_active":podname_active,
                "pod_name_standby":podname_standby,
                "oam_ip": podip,
                "oam_port": "2222",
                "cmd_prompt": prompt[-1][1:],
                "flash_name": flash,
                "S5S8-Loopback": ip_ranges
         }
    #print("data is", data)
    print_log(request_id,f'Requested data is : {data}',level_info)
    return data