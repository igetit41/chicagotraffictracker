#pip install pika
#pip install psycopg2

import os
import time
import json

import pika
import psycopg2

#Rabbitmq server connection
parameters = pika.ConnectionParameters(credentials=pika.PlainCredentials(os.environ['rabbitServer_mqadmin'], os.environ['rabbitServer_mqadminpassword']), host=os.environ['rabbitServer'], port=5672)

rabbitmq_conn = pika.BlockingConnection(parameters=parameters)
channel = rabbitmq_conn.channel()
channel.exchange_declare(exchange='processedData',exchange_type='fanout')
channel.queue_declare(queue='dbstream_postgresql')
channel.queue_bind(exchange='processedData', queue='dbstream_postgresql')

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

#Consume callback
def callback(ch, method, properties, body):
    print("Received %r" % body)
    infoBlock = json.loads(body)

    #Create table if it does not exist
    cursor.execute("select * from information_schema.tables where table_name=%s", ('chicagotrafficstats',))
    tablecheck = cursor.fetchall()

    if len(tablecheck) < 1:
        cursor.execute('CREATE TABLE chicagoTrafficStats (dateAdded timestamp, segmentid int, _strheading varchar(255), _traffic int, _tost varchar(255), _fromst varchar(255), _last_updt timestamp, _length float8, street varchar(255), _direction varchar(255), _lif_lat float8, start_lon float8, _lit_lat float8, _lit_lon float8, comments text)')
        postgresql_conn.commit()
        print('Table created.')
    
    #Insert data into PostgreSQL db
    cursor.execute("""INSERT INTO chicagoTrafficStats (dateAdded, segmentid, _strheading, _traffic, _tost, street, _last_updt, _length, _fromst, _direction, _lif_lat, start_lon, _lit_lat, _lit_lon, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(infoBlock['dateAdded'], infoBlock['segmentid'], infoBlock['_strheading'], infoBlock['_traffic'], infoBlock['_tost'], infoBlock['street'], infoBlock['_last_updt'], infoBlock['_length'], infoBlock['_fromst'], infoBlock['_direction'], infoBlock['_lif_lat'], infoBlock['start_lon'], infoBlock['_lit_lat'], infoBlock['_lit_lon'], infoBlock['comments']))
    postgresql_conn.commit()
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++iteration')

channel.basic_consume(callback, queue='dbstream_postgresql', no_ack=True)

#Start consuming
print('Script Running')
channel.start_consuming()

