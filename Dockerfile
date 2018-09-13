FROM python:3

ADD amqp_producer.py /

RUN pip install pika
RUN pip install pyaudio

CMD [ "python", "./amqp_producer.py" ]