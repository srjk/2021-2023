import json
from kafka import KafkaProducer
import sys
from datetime import datetime

result=sys.argv[1]
kafka_pod=sys.argv[2]
kafka_topic=sys.argv[3]
order_id=sys.argv[4]

result=result.split(",")


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

# topic='nflcmLog'
# broker = 'ib-orc-strimzi-001-kafka-bootstrap.use1az1n001d1-ns-ib-orc001:9092'
broker=kafka_pod
topic=kafka_topic
message_producer = MessageProducer(broker,topic)
# order_id="444631532"
data = {'@timestamp':'','@version':'1','message':'','external_request_id': order_id,'level':'INFO'}




for i in result:
   data["message"]=i
   var= datetime.utcnow().isoformat()[:-3]+'Z'
   data["@timestamp"]=var
   print(data)
   message_producer.send_msg(data)

data = {'@timestamp':'','@version':'1','message':'All pods are up and running','external_request_id': order_id,'level':'INFO'}
var= datetime.utcnow().isoformat()[:-3]+'Z'
data["@timestamp"]=var
message_producer.send_msg(data)