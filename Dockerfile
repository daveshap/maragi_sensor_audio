FROM python:3.6

ADD amqp_producer.py /

RUN pip install pika

CMD [ "python", "./amqp_producer.py" ]