FROM maragi_mic

ADD amqp_pub.py /

CMD [ "python3", "./amqp_pub.py" ]
