#pip install pika
#pip install google-cloud-bigquery

from google.cloud import bigquery
import pika
import os
import time
import datetime
import json

#Rabbitmq server connection
parameters = pika.ConnectionParameters(credentials=pika.PlainCredentials(os.environ['rabbitServer_mqadmin'], os.environ['rabbitServer_mqadminpassword']), host=os.environ['rabbitServer'], port=5672)
rabbitmq_conn = pika.BlockingConnection(parameters=parameters)
channel = rabbitmq_conn.channel()

channel.exchange_declare(exchange='processedData',exchange_type='fanout')
channel.queue_declare(queue='dbstream_bigquery')
channel.queue_bind(exchange='processedData', queue='dbstream_bigquery')

#channel.queue_declare(queue='bigquery')

#bigquery connection
client = bigquery.Client.from_service_account_json(os.environ['bigquery_creds'])

def callback(ch, method, properties, body):
    print("Received %r" % body)

    infoBlock = json.loads(body)
    bigqformat = [{}]

    bigqformat[0]['dateAdded'] = time.mktime(datetime.datetime.strptime(infoBlock['dateAdded'], "%Y-%m-%d %H:%M:%S.%f%z").timetuple())
    bigqformat[0]['segmentid'] = int(infoBlock['segmentid'])
    bigqformat[0]['_strheading'] = infoBlock['_strheading']
    bigqformat[0]['_traffic'] = int(infoBlock['_traffic'])
    bigqformat[0]['_tost'] = infoBlock['_tost']
    bigqformat[0]['street'] = infoBlock['street']
    bigqformat[0]['_last_updt'] = time.mktime(datetime.datetime.strptime(infoBlock['_last_updt'], "%Y-%m-%d %H:%M:%S.%f%z").timetuple())
    bigqformat[0]['_length'] = float(infoBlock['_length'])
    bigqformat[0]['_fromst'] = infoBlock['_fromst']
    bigqformat[0]['_direction'] = infoBlock['_direction']
    bigqformat[0]['_lif_lat'] = float(infoBlock['_lif_lat'])
    bigqformat[0]['start_lon'] = float(infoBlock['start_lon'])
    bigqformat[0]['_lit_lat'] = float(infoBlock['_lit_lat'])
    bigqformat[0]['_lit_lon'] = float(infoBlock['_lit_lon'])
    bigqformat[0]['comments'] = infoBlock['comments']

    errors = client.insert_rows(client.get_table(client.dataset('trafficdata').table('chicagodata')), bigqformat)

    print(bigqformat)
    print(errors)
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++iteration')

#channel.basic_consume(callback, queue='bigquery', no_ack=True)
channel.basic_consume(callback, queue='dbstream_bigquery', no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()