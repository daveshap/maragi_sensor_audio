FROM maragi_mic

ADD amqp_producer.py /

CMD [ "python3", "./amqp_producer.py" ]