FROM python:3.6

ADD amqp_producer.py /

RUN apt-get install gcc \
    pip install pika \
    pip install pyaudio

CMD [ "python", "./amqp_producer.py" ]