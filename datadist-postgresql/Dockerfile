#pythonDBPopulate
FROM python:3.7.1-stretch
ADD datadist-postgresql.py .
ADD gcppostgresslclient-cert.pem .
ADD gcppostgresslclient-key.pem .
ADD gcppostgresslserver-ca.pem .

RUN pip install pika
RUN pip install psycopg2
RUN pip install python-dateutil
RUN useradd postgres
RUN chown postgres ./gcppostgresslclient-key.pem
RUN chgrp postgres ./gcppostgresslclient-key.pem
RUN chmod 600 ./gcppostgresslclient-key.pem
CMD python datadist-postgresql.py
