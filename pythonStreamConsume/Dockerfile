#pythonStreamConsume
FROM python:3.7.1-stretch
ADD pythonStreamConsume.py .

RUN pip install pika
RUN pip install sodapy
CMD python pythonStreamConsume.py
