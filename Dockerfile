FROM python:3.6

ADD amqp_producer.py /

RUN apt-get install libasound2-dev
RUN pip install pika
RUN pip install pyalsaaudio
RUN pip install time
RUN pip install audioop

CMD [ "python", "./amqp_producer.py" ]