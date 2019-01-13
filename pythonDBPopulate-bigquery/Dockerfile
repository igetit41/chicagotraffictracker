#pythonDBPopulate
FROM python:3.7.1-stretch
ADD pythonDBPopulate-bigquery.py .
ADD bigquerycreds.json .

RUN pip install pika
RUN pip install google-cloud-bigquery
CMD python pythonDBPopulate-bigquery.py
