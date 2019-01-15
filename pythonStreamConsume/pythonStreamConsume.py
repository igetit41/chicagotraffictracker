#pip install pika
#pip install sodapy

import os
import time
import json

import pika
from sodapy import Socrata

#Rabbitmq server connection
parameters = pika.ConnectionParameters(credentials=pika.PlainCredentials(os.environ['rabbitServer_mqadmin'], os.environ['rabbitServer_mqadminpassword']), host=os.environ['rabbitServer'], port=5672)
rabbitmq_conn = pika.BlockingConnection(parameters=parameters)

channel = rabbitmq_conn.channel()
channel.queue_declare(queue='rawData')
rabbitmq_conn.close()

#Data stream connection
client = Socrata(os.environ['stream_url'], os.environ['stream_token'], username=os.environ['stream_account'], password=os.environ['stream_password'])

print("Stream Started")

while True:
    results = client.get("8v9j-bter", limit=10000)
    rabbitmq_conn = pika.BlockingConnection(parameters=parameters)
    channel = rabbitmq_conn.channel()

    #Split the batch data into individual rows
    for i in range(len(results)):
        infoBlock = json.dumps(results[i])
        channel.basic_publish(exchange='', routing_key='rawData', body=infoBlock)
        print(infoBlock)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++iteration')
    
    rabbitmq_conn.close()
    time.sleep(600)
