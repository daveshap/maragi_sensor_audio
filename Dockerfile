FROM python:3.6

ADD amqp_producer.py /

RUN apt-get install python3-pyaudio libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
RUN apt-get install ffmpeg libav-tools
RUN pip install pika
RUN pip install pyaudio

CMD [ "python", "./amqp_producer.py" ]