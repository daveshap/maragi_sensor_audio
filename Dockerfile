FROM python:3
ADD amqp_producer.py /
RUN pip install requirements.txt
CMD [ "python", "./amqp_producer.py" ]