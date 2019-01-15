#pip install pika
#pip install psycopg2
#pip install python-dateutil

import os
import time
import datetime
import dateutil
import dateutil.parser
import json

import pika
import psycopg2

#Rabbitmq server connection
parameters = pika.ConnectionParameters(credentials=pika.PlainCredentials(os.environ['rabbitServer_mqadmin'], os.environ['rabbitServer_mqadminpassword']), host=os.environ['rabbitServer'], port=5672)

rabbitmq_conn = pika.BlockingConnection(parameters=parameters)
channel = rabbitmq_conn.channel()
channel.exchange_declare(exchange='processedData',exchange_type='fanout')
channel.queue_declare(queue='rawData')

#PostgreSQL connection
postgresql_conn = psycopg2.connect(
    host = os.environ['postgreSQL_host'],
    port = 5432,
    user = os.environ['postgreSQL_user'],
    password = os.environ['postgreSQL_password'],
    sslmode = 'verify-ca',
    sslrootcert = os.environ['postgreSQL_sslrootcert'],
    sslcert = os.environ['postgreSQL_sslcert'],
    sslkey = os.environ['postgreSQL_sslkey'],
    database = os.environ['postgreSQL_database'])

cursor = postgresql_conn.cursor()

#Create table if it does not exist
cursor.execute("select * from information_schema.tables where table_name=%s", ('chicagotrafficstats',))
tablecheck = cursor.fetchall()

if len(tablecheck) < 1:
    cursor.execute('CREATE TABLE chicagoTrafficStats (dateAdded timestamp, segmentid int, _strheading varchar(255), _traffic int, _tost varchar(255), _fromst varchar(255), _last_updt timestamp, _length float8, street varchar(255), _direction varchar(255), _lif_lat float8, start_lon float8, _lit_lat float8, _lit_lon float8, comments text)')
    postgresql_conn.commit()
    print('Table created.')

#Consume callback
def callback(ch, method, properties, body):
    print("Received %r" % body)
    processedData = json.loads(body)

    #Add comments if none are present
    if 'comments' not in processedData:
        processedData['comments'] = ""

    #Convert time to UTC
    dateAdded = datetime.datetime.now()
    dateAdded = dateAdded.replace(tzinfo=dateutil.tz.gettz('UTC'))
    processedData['dateAdded'] = dateAdded.strftime('%Y-%m-%d %H:%M:%S.%f%z')

    _last_updt = datetime.datetime.strptime(processedData['_last_updt'], "%Y-%m-%d %H:%M:%S.%f")
    _last_updt = _last_updt.replace(tzinfo=dateutil.tz.gettz('America/Chicago'))
    _last_updt = _last_updt.astimezone(dateutil.tz.gettz('UTC'))
    processedData['_last_updt'] = _last_updt.strftime('%Y-%m-%d %H:%M:%S.%f%z')
    
    #Check DB for duplicate data
    cursor.execute('SELECT * FROM chicagoTrafficStats WHERE _strheading = %s AND _traffic = %s AND _tost = %s AND street = %s AND _last_updt = %s AND _length = %s AND _fromst = %s AND _direction = %s AND _lif_lat = %s AND start_lon = %s AND _lit_lat = %s AND _lit_lon = %s',(processedData['_strheading'], processedData['_traffic'], processedData['_tost'], processedData['street'], processedData['_last_updt'], processedData['_length'], processedData['_fromst'], processedData['_direction'], processedData['_lif_lat'], processedData['start_lon'], processedData['_lit_lat'], processedData['_lit_lon']))

    rows = len(cursor.fetchall())

    #Publish if data is unique
    if rows < 1:
        channel.basic_publish(exchange='processedData', routing_key='', body=json.dumps(processedData))
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++newInfo')

    print('++++++++++++++++++++++++++++++++++++++++++++++++++++iteration')

#Declare consume parameters
channel.basic_consume(callback, queue='rawData', no_ack=True)

#Start consuming
print('Script Running')
channel.start_consuming()

