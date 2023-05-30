import uuid
import boto3
from datetime import datetime
from datetime import date
from time import strftime
from time import sleep
import os
import logging
from fpdf import FPDF
from app.update_status_db import update_status


def push_s3(data, folder_name, logfile):

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
        assumed = sts.assume_role(RoleArn=s3_role,RoleSessionName="mysession",DurationSeconds=900)#def push_s3(operation, s3_role, s3_bucket, s3_input_dir):
        #print("assumed ==", assumed)
        credentials = assumed["Credentials"]
        #print(credentials)

        os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
        os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
        os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']

        # print("now printing env variable")
        # print(os.environ['AWS_ACCESS_KEY_ID'])

        # print(os.environ['AWS_SECRET_ACCESS_KEY'])
        # print(os.environ['AWS_SESSION_TOKEN'])
    except Exception as e:
        print (e)
        desc=e
        status="Failure"
        return status


    print("NOW enetered push s3")

    operation=data["operation"]

    print("operation ==", operation)

 #   logfile=''
    bucket_name=s3_input_dir

    print("bucket name is ", bucket_name)

    first_string_after_slash = bucket_name.split('//')[1]
    first_string_till_next_slash = first_string_after_slash.split('/')[0]
    print("*******",first_string_after_slash)
    print(first_string_till_next_slash)

    new_bucket_name=first_string_till_next_slash


    print("new bucket name ==", new_bucket_name)

    second_string_after_second_slash = first_string_after_slash.split('/',1)[1]
    print("^^^^^^^^^^^^^^^^^^^^^^^",second_string_after_second_slash)  # prints "more"
    new_object_name=second_string_after_second_slash

#     if operation == "precheck":
#          logfile=logfile_pre
#          print("precheck", logfile)
#     elif operation == "postcheck":
#          logfile=logfile_post
#          print("ppostheck", logfile)

    print("log file is ", logfile)
    object_name=new_object_name+"/"+folder_name+"/"+logfile
    final_s3_object=new_object_name+"/"+folder_name

    print("object name is", object_name)


    s3 = boto3.client('s3')
    # print("now printing env variable at the end")
    # print(os.environ['AWS_ACCESS_KEY_ID'])

    # print(os.environ['AWS_SECRET_ACCESS_KEY'])
    # print(os.environ['AWS_SESSION_TOKEN'])

    bucket_exists = True
    try:
        s3.head_bucket(Bucket=new_bucket_name)
    except Exception as e:
    #except botocore.exceptions.ClientError as e:

        # If the bucket does not exist, create it
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
                s3.create_bucket(Bucket=new_bucket_name)
                bucket_exists = False

    #push the pdf to S3
    s3 = boto3.client('s3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            aws_session_token=os.environ['AWS_SESSION_TOKEN']
            )


    try:
            if operation == "precheck":
               logfile="/tmp/"+str(request_id)+"_output"+"/"+logfile
               response = s3.upload_file(logfile, new_bucket_name, object_name)
               print(f"Uploaded to S3 {response}")
               fileurl=f's3://{new_bucket_name}.s3.amazonaws.com/{object_name}'
               print(fileurl)
               local_path='/tmp/'+str(request_id)+"_output/"
               for filename in os.listdir(local_path):
                   if filename.endswith('.cfg') or filename.endswith('.dat') or filename.endswith('.tar') or filename.endswith('.log'):
                       filepath = os.path.join(local_path, filename)
                       print(filepath)
                       object_name_cfg=new_object_name+"/"+folder_name+"/"+filename
                       with open(filepath, 'rb') as f:
                               print("uploading the .cfg file")
                               s3.upload_file(filepath, new_bucket_name, object_name_cfg)
                       fileurlcfg=f's3://{new_bucket_name}.s3.amazonaws.com/{object_name_cfg}'
                       print(f'Uploaded {filename} to {fileurlcfg}')
                       status="Success"
                       desc="Success"
            
            if operation == "postcheck":   
               logfile="/tmp/"+str(request_id)+"_output"+"/"+logfile
               response = s3.upload_file(logfile, new_bucket_name, object_name)
               print(f"Uploaded to S3 {response}")
               fileurl=f's3://{new_bucket_name}.s3.amazonaws.com/{object_name}'
               print(fileurl)
               local_path='/tmp/'+str(request_id)+"_output/"
               for filename in os.listdir(local_path):
                   if filename.endswith('.cfg') or filename.endswith('.dat') or filename.endswith('.tar') or filename.endswith('.log'):
                       filepath = os.path.join(local_path, filename)
                       object_name_cfg=new_object_name+"/"+folder_name+"/"+filename
                       with open(filepath, 'rb') as f:
                               print("uploading the .cfg file")
                               s3.upload_file(filepath, new_bucket_name, object_name_cfg)
                       fileurlcfg=f's3://{new_bucket_name}.s3.amazonaws.com/{object_name_cfg}'
                       print(f'Uploaded {filename} to {fileurlcfg}')
                       status="Success"
                       desc="Success"
            

            #os.remove("/code/std.log")
            #print("deleted the log file")

    except Exception as e:
            print("*********************************")
            logging.error(e)
            status="Failure"
            print("status after pushing is ", status)
    finally:
        #print("in finally block")
        print("status is ==", status)
        return status 
        """
        data={
                        "request_id":request_id,
                        "s3_dir": final_s3_object,
                        "request_status": status,
                        "desc": status
        }
        update_status(data)
        """