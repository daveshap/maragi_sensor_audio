import pyaudio
import pika


def publish_audio():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0'))
    channel = connection.channel()
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    print('audio stream is open')
    while True:
        frame = stream.read(4000)
        channel.basic_publish(exchange='sensor_audio', body=frame.hex(), routing_key='')


if __name__ == "__main__":
    while True:
        try:
            publish_audio()
        except Exception as oops:
            print('ERROR', oops)
