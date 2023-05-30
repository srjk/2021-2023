import boto3
import json
import sys
import os
import time
from kafka import KafkaProducer
from datetime import datetime

response=''
id=''

content=''
f=open('/tmp/test')
data = json.load(f)
f.close()

repo_name=data["config_context"]["codeCommitRepo"]
deploy_env=data["config_context"]["deploy_env"]
#print(repo_name)
pname="pipeline-"+ deploy_env
pipeline_name=repo_name.replace("repo",pname)
#print(pipeline_name)

# filename= sys.argv[1]
role= sys.argv[1]
session_name=sys.argv[2]
region_name=sys.argv[3]
kafka_pod=sys.argv[4]
kafka_topic=sys.argv[5]
order_id=sys.argv[6]

def role_arn_to_session(rolearn,roles):
    """
    Usage :
        session = role_arn_to_session(
            RoleArn='arn:aws:sts::147415857303:assumed-role/Create-CNFM-Lambda-Role-us-east-1',
            RoleSessionName='botocore-session-1667933169')
        client = session.client('sqs')
    """
    client = boto3.client('sts')
    response = client.assume_role( RoleArn=rolearn,RoleSessionName=roles)
    return boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'],
        region_name=region_name)
session=role_arn_to_session(role,session_name)
# #print(boto3.Session())
client = session.client('codecommit')

response = client.get_branch(
    repositoryName=repo_name,
    branchName='dev'
)
response = client.get_commit(
    repositoryName=repo_name,
    commitId=response['branch']['commitId']
)
response = client.create_branch(
    repositoryName=repo_name,
    branchName='temp',
    commitId=response['commit']['commitId']
)


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
path_repo='config/'+ deploy_env+ '/'+profile_name+'/'
f=open('/tmp/test')
data = json.load(f)
f.close()
#print(type(data))
#print("000000000000000000")
#print(data)
data["config_context"]['application_json']["profiles"][profile_name]["install_mode"]="terminate"
content= '' + json.dumps(data["config_context"]['application_json'],indent=2) +''
putFiles_dummy={
            'filePath': '',
            'fileMode': 'NORMAL',
            'fileContent': content
        }
putFiles_dummy["filePath"]=path_repo+'application_config.json'
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
#print(response)
##print(json_config['cnfPackageVersionFile']!=data_config['cnfPackageVersionFile'])
#if json_config['cnfPackageVersionFile']!=data_config['cnfPackageVersionFile']:
# test(response)
commitId=response["commitId"]
response = client.merge_branches_by_fast_forward(
    repositoryName=repo_name,
    sourceCommitSpecifier='temp',
    destinationCommitSpecifier='dev',
    targetBranch='dev'
)

response = client.delete_branch(
    repositoryName=repo_name,
    branchName='temp'
)

#print("+++++++++++++++++++++++")

#print(response)



client = session.client('codepipeline')

response = client.get_pipeline(
    name=pipeline_name
)

##print(response)

time.sleep(125)
response = client.list_pipeline_executions(
    pipelineName=pipeline_name,
    maxResults=5,
)

for i in response['pipelineExecutionSummaries']:
   if (i['sourceRevisions'][0]['revisionId'] == commitId):

     #print(i['pipelineExecutionId'])
     id=i['pipelineExecutionId']
     response_status=i['status']




#pipeline_name=sys.argv[1]
# response_status=sys.argv[3]
# commitId= sys.argv[4]
# role = sys.argv[5]
# session_name=sys.argv[6]
f=open('/tmp/test')
data = json.load(f)
f.close()

repo_name=data["config_context"]["codeCommitRepo"]
#print(repo_name)
# pipeline_name=repo_name.replace("repo","pipeline-dev")
#order_id= data["custom_fields"]["lcm_orderId"]
response=''
# id=sys.argv[2]
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
while(buildstatus=="InProgress"):
  response = cp.get_pipeline_state(
    name=pipeline_name,
  )

  if(response["stageStates"][1]["latestExecution"]["pipelineExecutionId"]==id):
    buildstatus=response["stageStates"][1]["latestExecution"]["status"]
    #print(buildstatus)
  cloudWatchLogclient = session.client('logs')
  cloudWatchResponse = cloudWatchLogclient.get_log_events(
            logGroupName=loggroupname, # Can be dynamic
            logStreamName=executionid,
            startTime=stime)

  #print(cloudWatchResponse)



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
if(buildstatus!='Succeeded'):
   sys.exit("Failed")

time.sleep(2)
sfstatus='status'
arn='string'
while(arn=='string'):
  response = cp.get_pipeline_state(
    name=pipeline_name,
  )

  if(response["stageStates"][2]["latestExecution"]["pipelineExecutionId"]==id):
    #print(response)
    sfstatus=response["stageStates"][2]["latestExecution"]["status"]
    arn=response["stageStates"][2]["actionStates"][0]["latestExecution"]["externalExecutionId"]
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
executionid=project.split(':')[1]
#print(projectname)
#print(executionid)



client = session.client('codebuild')
response = client.batch_get_projects(
    names=[
        projectname,
    ]
)

loggroupname=response["projects"][0]["logsConfig"]["cloudWatchLogs"]["groupName"]
#print(loggroupname)
sfstatus=="InProgress"
time.sleep(2)
stime=123
while(sfstatus=="InProgress"):
  response = cp.get_pipeline_state(
    name=pipeline_name,
  )

  if(response["stageStates"][2]["latestExecution"]["pipelineExecutionId"]==id):
    sfstatus=response["stageStates"][2]["latestExecution"]["status"]
    #print(sfstatus)
  cloudWatchLogclient = session.client('logs')
  cloudWatchResponse = cloudWatchLogclient.get_log_events(
            logGroupName=loggroupname, # Can be dynamic
            logStreamName=executionid,
            startTime=stime)

  #print(cloudWatchResponse)



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
