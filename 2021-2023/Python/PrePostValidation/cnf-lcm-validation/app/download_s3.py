import uuid
import boto3
from datetime import datetime
from datetime import date
from time import strftime
from time import sleep
import os
import logging
#from fpdf import FPDF
#from app.update_status_db import update_status


def download_s3(data):
    request_id=data["request_id"]
    deploy_env=data["deploy_env"]
    status="Success"
    try:
#        s3_bucket="s3://ib-orc-test3-validation/dev/nokia/upfd/usw2-az1-dev-smf01"
        s3_role=data["s3_data"]["s3_role"]
        s3_bucket=data["s3_data"]["s3_bucket"]
        s3_input_dir=data["s3_data"]["s3_input_dir"]
#        s3_role="arn:aws:iam::268785957902:role/na4d-s3bucket-execution"
        sts = boto3.client("sts")
        assumed = sts.assume_role(RoleArn=s3_role,RoleSessionName="mysession")#def push_s3(operation, s3_role, s3_bucket, s3_input_dir):
        # print("assumed ==", assumed)
        credentials = assumed["Credentials"]
        # print(credentials)

        os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
        os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
        os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']

        # print("now printing env variable")
        # print(os.environ['AWS_ACCESS_KEY_ID'])

        # print(os.environ['AWS_SECRET_ACCESS_KEY'])
        # print(os.environ['AWS_SESSION_TOKEN'])
        s3 = boto3.client('s3',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                aws_session_token=os.environ['AWS_SESSION_TOKEN']
                )
    except Exception as e:
        print (e)
        desc=e
        status="Failure"
        return status    

    try:
        # Specify the S3 bucket and folder prefix
        bucket_name = s3_bucket
        prefix = s3_input_dir.replace("s3://"+s3_bucket+'/','')+"/"
        print(prefix)

        # Get a list of all objects in the folder
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        #print(response)
        # Sort the objects by last modified time
        objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'], reverse=True)

        # Get the last modified folder
        print(objects[0])
        last_modified_folder = objects[0]['Key'].split('/')[:-1]
        last_modified_folder='/'.join(last_modified_folder) + '/'
        print("Last modified folder:", last_modified_folder)
        file_path=last_modified_folder.replace("s3://"+s3_bucket+'/','')+"precheck_admin_save.cfg"
        print(file_path)
        try:  
          response=s3.head_object(Bucket=s3_bucket,Key=file_path)
        except s3.exceptions.ClientError as e:
              status="false"
              return status
        s3.download_file(s3_bucket, file_path, '/tmp/'+str(request_id)+'_output/precheck_admin_save.cfg')
        return status
    except Exception as e:
        print(e)
        status="Failure"
        return status
#download_s3(data)
