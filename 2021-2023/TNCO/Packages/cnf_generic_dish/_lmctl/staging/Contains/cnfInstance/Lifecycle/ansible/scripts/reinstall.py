import boto3
import json
import sys
import os
import time
from kafka import KafkaProducer
from datetime import datetime
from botocore.config import Config
import botocore

config = Config(
   retries = {
      'max_attempts': 10,
      'mode': 'standard'
   }
)
response=''
id=''

content=''
f=open('/tmp/test')
data = json.load(f)
f.close()

repo_name=data["config_context"]["codeCommitRepo"]
deploy_env=data["config_context"]["deploy_env"]
order_id= data["custom_fields"]["lcm_orderId"]
#print(repo_name)
pname="pipeline-"+ deploy_env
pipeline_name=repo_name.replace("repo",pname)
#print(pipeline_name)

filename= sys.argv[1]
role= sys.argv[2]
session_name=sys.argv[3]
region_name=sys.argv[4]
kafka_pod=sys.argv[5]
kafka_topic=sys.argv[6]
#print(filename)
# tarfilename= filename + ".tar"
# #print(tarfilename)
# import tarfile
# my_tar = tarfile.open(tarfilename)
# my_tar.extractall(filename) # specify which folder to extract to
# my_tar.close()

def role_arn_to_session(rolearn,roles):
    client = boto3.client('sts')
    response = client.assume_role( RoleArn=rolearn,RoleSessionName=roles)
    return boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'],
        region_name=region_name)
session=role_arn_to_session(role,session_name)
# #print(boto3.Session())


class MessageProducer:                                                                                  
    broker = ""                                                                                         
    topic = ""                                                                                          
    producer = None                                                                                     
                                                                                                        
    def __init__(self, broker, topic):                                                                  
        self.broker = broker                                                                            
        self.topic = topic                                                                              
        self.producer = KafkaProducer(bootstrap_servers=self.broker,                                    
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),                                       
        acks='all',                                                                                     
        retries = 3)                                                                                    
                                                                                                        
                                                                                                        
    def send_msg(self, msg):                                                                            
        #print("sending message...")                                                                    
        try:                                                                                            
            future = self.producer.send(self.topic,msg)                                                 
            self.producer.flush()                                                                       
            future.get(timeout=60)                                                                      
            #print("message sent successfully...")                                                      
            return {'status_code':200, 'error':None}                                                    
        except Exception as ex:                                                                         
            return ex                                                                                   
                                                                                                        
                                                                                                        
#broker = 'ib-orc-strimzi-001-kafka-bootstrap.use1az1n001d1-ns-ib-orc001:9092'                          
broker=kafka_pod                                                                                        
topic=kafka_topic                                                                                       
message_producer = MessageProducer(kafka_pod,kafka_topic)

def send_kafka(data,msg):
      data["message"]=msg                                                                               
      var= datetime.utcnow().isoformat()[:-3]+'Z'                                                                                                                                      
      data["@timestamp"]=var                                                                            
      return data
def check_log_stream_exists(log_group_name, log_stream_name):
    try:
        client=session.client("logs")
        response = client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            startTime=1
        )
        return True
    except Exception as e:
        # print(f"Error: {e}")
        return False

def main(log_group_name, log_stream_name, retries=30, sleep_time=5):
    exists = False
    attempt = 0
    while not exists and attempt < retries:
        exists = check_log_stream_exists(log_group_name, log_stream_name)
        # print(attempt)
        if not exists:
            attempt += 1
            data = {'@timestamp':'','@version':'1','message':'','external_request_id': order_id,'level':'INFO'}
            msg="number of attempt for log stream" + str(attempt)                                                            
            message_producer.send_msg(send_kafka(data, msg))
            time.sleep(sleep_time)
    return exists
def cloudwatchlogprint(status,number,data,id):
    step2=0
    stime=123
    while(status=="InProgress"):
      response = cp.get_pipeline_state(
        name=pipeline_name,
      )

      if(response["stageStates"][number]["latestExecution"]["pipelineExecutionId"]==id):
        status=response["stageStates"][number]["latestExecution"]["status"]
        #print(sfstatus)
      while(step2 < 1):
        # print("inside while ")
        exists = main(loggroupname, executionid)
        if exists:
          # print("inside if")
          step2=2
          break
        else:
          sys.exit("log stream not found")
      #print(cloudWatchResponse)


      cloudWatchLogclient = session.client('logs',config=config)                                        
      cloudWatchResponse = cloudWatchLogclient.get_log_events(                                          
                    logGroupName=loggroupname, # Can be dynamic                                             
                    logStreamName=executionid,                                                         
                    startTime=stime) 
      for i in cloudWatchResponse["events"]:
        stime=i["timestamp"]+2
        #print("****")                                                                                                                                                 
        if not i["message"].isspace():
          doc = i["message"].split('\n')
          doc = " ".join(doc)
          doc = doc.replace('"','\'')                                                                                                                                  
          data["message"]=doc
          var= datetime.utcnow().isoformat()[:-3]+'Z'
        #   var1="'"+ var+"'"
          data["@timestamp"]=var
          message_producer.send_msg(data)
          #print(doc)
      time.sleep(2)
    return status


client = session.client('codecommit')

response = client.get_branch(
    repositoryName=repo_name,
    branchName='dev'
)
response = client.get_commit(
    repositoryName=repo_name,
    commitId=response['branch']['commitId']
)
try:
  response = client.create_branch(
      repositoryName=repo_name,
      branchName='temp',
      commitId=response['commit']['commitId']
    )
except client.exceptions.BranchNameExistsException as error:
  response1 = client.delete_branch(
    repositoryName=repo_name,
    branchName='temp'
  )
  response = client.create_branch(
      repositoryName=repo_name,
      branchName='temp',
      commitId=response['commit']['commitId']
    )

def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.
full_file_paths = get_filepaths(filename)
putFileContent=[]
putFiles_dummy={
            'filePath': '',
            'fileMode': 'NORMAL',
            'fileContent': content
        }
content=''
#print("_____________")
#print(data)
profile_n=data["config_context"]['application_json']['profiles'].keys()


#print(profile_n)
profile_name=''
for key in profile_n:
  profile_name=key
#path_repo='config/'+ deploy_env+ '/'+profile_name+'/'
path_repo='config/'+ deploy_env+ '/'+profile_name.replace("_","-")+'/'
new_list=[]
list_directory=[]
for f in os.listdir(filename):
  if '_values' in f:
    list_directory.append(f)
#print(list_directory)
filearray=["Chart.yaml","values.yaml"]
result= [i for i in list_directory if not any([e for e in filearray if e in i])]
#print(result)
folder_path=path_repo+'values'
path=filename + "/"+result[0]
with open(path) as f:
        while True:
          line = f.readline()
          if not line:
            break
          for l in line:
            content=content+l
        ##print(content)
putFiles_dummy["filePath"]=path.replace(filename,folder_path)
putFiles_dummy["fileContent"]=content
content=''
putFileContent.append(putFiles_dummy)
putFiles_dummy={
            'filePath': '',
            'fileMode': 'NORMAL',
            'fileContent': content
        }
filearray=["license","config","values.yaml","cmm-provisioning.yaml","cmg_alarms.csv"]
result= [i for i in full_file_paths if any([e for e in filearray if e in i])]
#print(result)
for fpath in result:
      fname=os.path.basename(fpath)
      folder_path=path_repo+'site_specific'
      if "cmm" in fpath:
        putFiles_dummy["filePath"]=folder_path + '/' + fname
      else:
        putFiles_dummy["filePath"]=fpath.replace(filename,folder_path)
      with open(fpath) as f:
        while True:
          line = f.readline()
          if not line:
            break
          for l in line:
            content=content+l
        ##print(content)
      putFiles_dummy["fileContent"]=content
      content=''
      putFileContent.append(putFiles_dummy)
      putFiles_dummy={
            'filePath': '',
            'fileMode': 'NORMAL',
            'fileContent': content
        }

#print(putFileContent)
#print("00000")
#print(response)

f=open('/tmp/test')
data = json.load(f)
f.close()
data["config_context"]['application_json']["profiles"][profile_name]["install_mode"]="reinstall"
content= '' + json.dumps(data["config_context"]['application_json'],indent=2) +''
putFiles_dummy={
            'filePath': '',
            'fileMode': 'NORMAL',
            'fileContent': content
        }
putFiles_dummy["filePath"]=path_repo+'application_config.json'
putFiles_dummy["fileContent"]=content
putFileContent.append(putFiles_dummy)


content= '' + json.dumps(data["config_context"]['config_json'],indent=2) +''
putFiles_dummy={
            'filePath': '',
            'fileMode': 'NORMAL',
            'fileContent': content
        }
putFiles_dummy["filePath"]=path_repo+'config.json'
putFiles_dummy["fileContent"]=content
putFileContent.append(putFiles_dummy)
response = client.get_branch(
    repositoryName=repo_name,
    branchName='dev'
)
response = client.get_commit(
    repositoryName=repo_name,
    commitId=response['branch']['commitId']
)

# def test(response):
try:
  response = client.create_commit(
                      repositoryName=repo_name,
                       branchName='temp',
                       parentCommitId=response['commit']['commitId'],
                       authorName='ALM',
                       email='ALM',
                       commitMessage='dev',
                       keepEmptyFolders=True,
                       putFiles=putFileContent
                       )
except client.exceptions.NoChangeException as error:
  sys.exit("nothing to commit")

#print(response)
##print(json_config['cnfPackageVersionFile']!=data_config['cnfPackageVersionFile'])
#if json_config['cnfPackageVersionFile']!=data_config['cnfPackageVersionFile']:
# test(response)

if(deploy_env=='dev'):
  BranchName='dev'
else:
  BranchName='master'
commitId=response["commitId"]
response = client.merge_branches_by_fast_forward(
    repositoryName=repo_name,
    sourceCommitSpecifier='temp',
    destinationCommitSpecifier='dev',
    targetBranch=BranchName
)

response = client.delete_branch(
    repositoryName=repo_name,
    branchName='temp'
)

#print("+++++++++++++++++++++++")

data = {'@timestamp':'','@version':'1','message':'','external_request_id': order_id,'level':'INFO'}
msg = "code commit is done with commit id " + str(commitId)                                     
message_producer.send_msg(send_kafka(data, msg)) 



client = session.client('codepipeline')

response = client.get_pipeline(
    name=pipeline_name
)

##print(response)

msg="sleep 60 seconds for pipeline to trigger"
message_producer.send_msg(send_kafka(data, msg))

time.sleep(60)
msg="number of iteration : 20 with 15 seconds delay to check pipeline trigger "                                                            
message_producer.send_msg(send_kafka(data, msg))
time_break = ''
time_period=0
while(time_break == ''):
  response = client.list_pipeline_executions(
    pipelineName=pipeline_name,
    maxResults=5,
  )

  for i in response['pipelineExecutionSummaries']:
     #print(i['sourceRevisions'])
     if ( len(i['sourceRevisions']) != 0):
       if (i['sourceRevisions'][0]['revisionId'] == commitId):

         #print(i['pipelineExecutionId'])
         id=i['pipelineExecutionId']
         response_status=i['status']
  time.sleep(15)
  time_period=time_period+1
  msg="number of iteration " + str(time_period) + " sleep  15 seconds"                                                            
  message_producer.send_msg(send_kafka(data, msg))
  if(id != '' or time_period == 20):
   msg="pipeline started with pipeline id " + str(id)                                     
   message_producer.send_msg(send_kafka(data, msg))
   break

if(id == ''):
  msg="pipeline id not found after 20 number of iteration "                                                
  message_producer.send_msg(send_kafka(data, msg))
  sys.exit("pipeline id not found")


data = {'@timestamp':'','@version':'1','message':'','external_request_id': order_id,'level':'INFO'}

cp = session.client(
    'codepipeline'
)


projectname='string'
#id='a42c87c2-f90c-41d2-b00a-8565737c6377'
buildstatus="start"
while(projectname=='string'):
  response = cp.get_pipeline_state(
    name=pipeline_name,
  )

  if(response["stageStates"][1]["latestExecution"]["pipelineExecutionId"]==id):
     projectname=response["stageStates"][1]["actionStates"][0]["latestExecution"]["externalExecutionId"]
     buildstatus=response["stageStates"][1]["latestExecution"]["status"]
     #print(buildstatus)
#print(projectname)


pname=projectname.split(':')[0]
executionid=projectname.split(":")[1]
#print(pname)
#print(executionid)

client = session.client('codebuild')
response = client.batch_get_projects(
    names=[
        pname,
    ]
)

loggroupname=response["projects"][0]["logsConfig"]["cloudWatchLogs"]["groupName"]
stime=123
step1=0
time.sleep(2)

buildstatus=cloudwatchlogprint(buildstatus,1,data,id)

if(buildstatus!='Succeeded'):
   sys.exit("Pre build Failed")
time.sleep(5)
sfstatus='status'
arn='string'
while(arn=='string'):
  response = cp.get_pipeline_state(
    name=pipeline_name,
  )
  if(len(response["stageStates"][2]) != 0): 
    if(response["stageStates"][2]["latestExecution"]["pipelineExecutionId"]==id):
      ##print(response)
      if(len(response["stageStates"][2]["actionStates"][0])!=0 and 'latestExecution' in response["stageStates"][2]["actionStates"][0] and 'externalExecutionId' in response["stageStates"][2]["actionStates"][0]["latestExecution"]):
        sfstatus=response["stageStates"][2]["latestExecution"]["status"]
        arn=response["stageStates"][2]["actionStates"][0]["latestExecution"]["externalExecutionId"]  
  # if(response["stageStates"][2]["latestExecution"]["pipelineExecutionId"]==id):
  #   #print(response)
  #   sfstatus=response["stageStates"][2]["latestExecution"]["status"]
  #   arn=response["stageStates"][2]["actionStates"][0]["latestExecution"]["externalExecutionId"]
    #print(sfstatus)
#print(arn)
client = session.client('stepfunctions')
sfbuildarn='status'
while(sfbuildarn=='status'):
  response= client.get_execution_history( executionArn=arn)
  for i in response["events"]:
    if "taskSubmittedEventDetails" in i.keys():
      sfbuildarn=json.loads(i["taskSubmittedEventDetails"]['output'])['Build']["Arn"]

project= sfbuildarn.split('/')[1]
projectname=project.split(':')[0]
executionid=''
executionid=project.split(':')[1]
# print(projectname)
# print(executionid)


client = session.client('codebuild')
response = client.batch_get_projects(
    names=[
        projectname,
    ]
)

loggroupname=response["projects"][0]["logsConfig"]["cloudWatchLogs"]["groupName"]
#print(loggroupname)
sfstatus=="InProgress"
time.sleep(10)
sfstatus=cloudwatchlogprint(sfstatus,2,data,id)

if(sfstatus!='Succeeded'):
   sys.exit("Step function Failed ")
#response= client.get_execution_history( executionArn=arn)
#print(response)
client = session.client('codepipeline')
response = client.list_pipeline_executions(
    pipelineName=pipeline_name,
    maxResults=5,
)

for i in response['pipelineExecutionSummaries']:
   if (i['sourceRevisions'][0]['revisionId'] == commitId):

     #print(i['pipelineExecutionId'])
     id=i['pipelineExecutionId']
     response_status=i['status']
print(response_status)
