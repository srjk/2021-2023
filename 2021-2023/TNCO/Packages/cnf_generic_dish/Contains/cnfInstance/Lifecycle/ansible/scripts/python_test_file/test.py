import boto3
import json
import mimetypes
import sys
import os
import time
response=''
id=''

content=''
f=open('/tmp/test')
data = json.load(f)
f.close()

repo_name=data["config_context"]["codeCommitRepo"]                                                   
#print(repo_name)                                                               
pipeline_name=repo_name.replace("repo","pipeline-dev")                                
#print(pipeline_name) 

filename= sys.argv[1]
role= sys.argv[2]
session_name=sys.argv[3] 
#print(filename)
tarfilename= filename + ".tar"
#print(tarfilename)
import tarfile
my_tar = tarfile.open(tarfilename)
my_tar.extractall(filename) # specify which folder to extract to
my_tar.close()

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
        aws_session_token=response['Credentials']['SessionToken'])
role_arn_to_session(role,session_name)
# #print(boto3.Session())
client = boto3.client('sts')
response = client.get_caller_identity(
)
client = boto3.client('codecommit')

response = client.get_branch(
    repositoryName=repo_name,
    branchName='master'
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

def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
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
            'filePath': 'config/dev/shubham/site_config',
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
path_repo='config/dev/'+profile_name+'/'
new_list=[]
list_directory=[]
for f in os.listdir(filename):              
  if '.yaml' in f:                                                         
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
            'filePath': 'config/dev/shubham/site_config',                                   
            'fileMode': 'NORMAL',                                                           
            'fileContent': content                       
        }
filearray=["license","config","values.yaml"]
result= [i for i in full_file_paths if any([e for e in filearray if e in i])]
#print(result)
for fpath in result:                                                    
      folder_path=path_repo+'site_specific'        
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
            'filePath': 'config/dev/shubham/site_config',
            'fileMode': 'NORMAL',                                                                  
            'fileContent': content
        }

#print(putFileContent)
#print("00000")
#print(response)

f=open('/tmp/test')
data = json.load(f)
f.close()
#print(type(data))
#print("000000000000000000")
#print(data)
content= '' + json.dumps(data["config_context"]['application_json'],indent=2) +''
putFiles_dummy={
            'filePath': 'config/dev/shubham/site_config',
            'fileMode': 'NORMAL',
            'fileContent': content
        }
putFiles_dummy["filePath"]=path_repo+'application.json'
putFiles_dummy["fileContent"]=content
putFileContent.append(putFiles_dummy)


content= '' + json.dumps(data["config_context"]['config_json'],indent=2) +''
putFiles_dummy={
            'filePath': 'config/dev/shubham/site_config',
            'fileMode': 'NORMAL',
            'fileContent': content
        }
putFiles_dummy["filePath"]=path_repo+'config.json'
putFiles_dummy["fileContent"]=content
putFileContent.append(putFiles_dummy)
response = client.get_branch(
    repositoryName=repo_name,
    branchName='master'
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
authorName='Devashish',
email='devashish',
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
    destinationCommitSpecifier='master',
    targetBranch='master'
)

response = client.delete_branch(
    repositoryName=repo_name,
    branchName='temp'
)

#print("+++++++++++++++++++++++")

#print(response)



client = boto3.client('codepipeline')

response = client.get_pipeline(
    name=pipeline_name
)

##print(response)

time.sleep(30)
response = client.list_pipeline_executions(
    pipelineName=pipeline_name,
    maxResults=5,
)

for i in response['pipelineExecutionSummaries']:
   if (i['sourceRevisions'][0]['revisionId'] == commitId):
    
     #print(i['pipelineExecutionId'])
     id=i['pipelineExecutionId']
     response_status=i['status']
print_content='{ "commitId": "'+ commitId +'","pipeline_id": "' +id+'","response_status": "'+ response_status+'"}'

print(json.loads(print_content))