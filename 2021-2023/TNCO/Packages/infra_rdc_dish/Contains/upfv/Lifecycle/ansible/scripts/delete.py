import boto3
import sys 
import time
import json
from kafka import KafkaProducer
from datetime import datetime
from botocore.config import Config
import botocore
role=sys.argv[1]
session_name=sys.argv[2]
region_name=sys.argv[3]
Sname=sys.argv[4]

kafka_pod=sys.argv[5]
kafka_topic=sys.argv[6]
order_id=sys.argv[7]


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
        ##print("sending message...")                                                                    
        try:                                                                                            
            future = self.producer.send(self.topic,msg)                                                 
            self.producer.flush()                                                                       
            future.get(timeout=60)                                                                      
            #print("message sent successfully...")                                                      
            return {'status_code':200, 'error':None}                                                    
        except Exception as ex:
            print(ex)                                                                         
            return ex                                                                                   
                                                                                                        
                                                                                                        
broker = 'ib-orc-strimzi-001-kafka-bootstrap:9092'                          
#broker=kafka_pod                                                                                        
#topic="nflcmLog" 
broker=kafka_pod                                                                                        
topic=kafka_topic                                                                                
message_producer = MessageProducer(broker,topic)

def send_kafka(data,msg):
      data["message"]=msg                                                                               
      var= datetime.utcnow().isoformat()[:-3]+'Z'                                                                                                                                      
      data["@timestamp"]=var                                                                            
      return data

data = {'@timestamp':'','@version':'1','message':'','external_request_id': order_id,'level':'INFO'}
msg = "Stack deletion initiated! " +str(Sname)                                  
message_producer.send_msg(send_kafka(data, msg)) 

client=session.client("cloudformation")
stack_name=Sname
events_response = client.describe_stack_events(StackName=stack_name)
next_token = None
"""
while next_token is not None:
      events_response = client.describe_stack_events(StackName=stack_name, NextToken=next_token)
      next_token = events_response.get('NextToken') 
"""

#print(events_response['StackEvents'][0]['EventId'])
response = client.delete_stack(
    StackName=Sname
)
#cloudformation_client = boto3.client('cloudformation')




#Sname=events_response['StackEvents'][0]['StackId']
stack_name = events_response['StackEvents'][0]['StackId']
msg="Stack deletion initiated! " +str(Sname)
message_producer.send_msg(send_kafka(data, msg))

last_event_id = events_response['StackEvents'][0]['EventId']
# Print events for the stack until it is deleted
while True:
    if next_token is not None:
        events_response = client.describe_stack_events(StackName=stack_name, NextToken=next_token)
    else:
        events_response =client.describe_stack_events(StackName=stack_name)
    next_token = events_response.get('NextToken')    
    for event in events_response['StackEvents']:
        if event['EventId'] == last_event_id:
            next_token=None
            break        
        if 'ResourceStatusReason' not  in event:
         msg= str(event['Timestamp']) + " - "+ str(Sname) +" - "+ str(event['ResourceType'])+ " - " +str(event['ResourceStatus'])
         message_producer.send_msg(send_kafka(data, msg))
         #print(f"{event['Timestamp']} - {event['ResourceType']} - {event['ResourceStatus']}")
        else:
          msg=str(event['Timestamp'])+ " - "+ str(Sname) +" - "+ str(event['ResourceType'])+ " - " +str(event['ResourceStatus'])
          message_producer.send_msg(send_kafka(data, msg))
          #print(f"{event['Timestamp']} - {event['ResourceType']} - {event['ResourceStatus']} - {event['ResourceStatusReason']}")
    if events_response['StackEvents']:
        last_event_id = events_response['StackEvents'][0]['EventId']    
        #print(last_event_id)
    # Check if the stack has been deleted
    stack_status = client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    if stack_status == 'DELETE_COMPLETE':
        msg= str(Sname) + " deleted successfully!"
        message_producer.send_msg(send_kafka(data, msg))
        print("Succeeded")
        break
    elif stack_status in ['DELETE_FAILED', 'ROLLBACK_COMPLETE']:
        print("Stack deletion failed!")
        break

    # Wait for a few seconds before checking again
    time.sleep(5)