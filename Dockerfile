FROM python:3.6

ADD amqp_producer.py /

RUN pip install pika
RUN pip install alsaaudio
RUN pip install time
RUN pip install audioop

#CMD [ "python", "./amqp_producer.py" ]