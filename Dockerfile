FROM maragi_mic

ADD amqp_producer.py /

CMD [ "python", "./amqp_producer.py" ]