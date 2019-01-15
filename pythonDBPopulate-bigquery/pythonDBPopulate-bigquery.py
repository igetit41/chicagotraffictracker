#pip install pika
#pip install google-cloud-bigquery

from google.cloud import bigquery
import pika
import os
import time
import datetime
import json

#BigQuery connection
bigquery_client = bigquery.Client.from_service_account_json(os.environ['bigquery_creds'])

#Create BigQuery structures if they do not exist
#Define dataset and table
dataset = bigquery_client.dataset('trafficdata')
table = dataset.table('chicagodata')

#Create dataset if it does not exist
try:
    bigquery_client.get_dataset(dataset)
except:
    dataset_ref = bigquery_client.create_dataset(bigquery.Dataset(dataset))
    print('Dataset created.')

#Create table if it does not exist
try:
    bigquery_client.get_table(table)
except:
    schema = [
        bigquery.SchemaField('dateAdded', 'TIMESTAMP', mode='REQUIRED'),
        bigquery.SchemaField('segmentid', 'INTEGER', mode='REQUIRED'),
        bigquery.SchemaField('_strheading', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('_traffic', 'INTEGER', mode='REQUIRED'),
        bigquery.SchemaField('_tost', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('_fromst', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('_last_updt', 'TIMESTAMP', mode='REQUIRED'),
        bigquery.SchemaField('_length', 'FLOAT', mode='REQUIRED'),
        bigquery.SchemaField('street', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('_direction', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('_lif_lat', 'FLOAT', mode='REQUIRED'),
        bigquery.SchemaField('start_lon', 'FLOAT', mode='REQUIRED'),
        bigquery.SchemaField('_lit_lat', 'FLOAT', mode='REQUIRED'),
        bigquery.SchemaField('_lit_lon', 'FLOAT', mode='REQUIRED'),
        bigquery.SchemaField('comments', 'STRING', mode='NULLABLE'),
    ]
    table_config = bigquery.Table(table, schema=schema)
    table_ref = bigquery_client.create_table(table_config)
    print('Table created.')


#Consume callback
def callback(ch, method, properties, body):
    print("Received %r" % body)
    channel.basic_ack(delivery_tag = method.delivery_tag)

    infoBlock = json.loads(body)

    #Process data into BigQuery format
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
    
    #Insert data into BigQuery
    errors = bigquery_client.insert_rows(bigquery_client.get_table(bigquery_client.dataset('trafficdata').table('chicagodata')), bigqformat)

    print(errors)
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++iteration')


#Brute force solution to timeouts due to BigQuery slow response times
connectionError = False
while connectionError != True:
    connectionError = True

    try:
        #Rabbitmq server connection
        parameters = pika.ConnectionParameters(credentials=pika.PlainCredentials(os.environ['rabbitServer_mqadmin'], os.environ['rabbitServer_mqadminpassword']), host=os.environ['rabbitServer'], port=5672, socket_timeout=5, connection_attempts=3, retry_delay=5)

        rabbitmq_conn = pika.BlockingConnection(parameters=parameters)
        channel = rabbitmq_conn.channel()
        channel.exchange_declare(exchange='processedData',exchange_type='fanout')
        channel.queue_declare(queue='dbstream_bigquery')
        channel.queue_bind(exchange='processedData', queue='dbstream_bigquery')

        channel.basic_consume(callback, queue='dbstream_bigquery', no_ack=False)

        print('Script Running')
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed:
        print("Connection Issues")
        connectionError = False
