import pyaudio
import pika


def get_usb_mic_idx():
    audio = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if 'USB' in info['name'] and 'Audio' in info['name']:
            return i
    exit('No USB audio devices detected. Please run container with --privileged')


def publish_audio(idx):
    print('opening audio stream')
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, input_device_index=idx)
    print('opening AMQP connection')
    parameters = pika.URLParameters('amqp://guest:guest@maragi-rabbit:5672/%2F')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    print('starting publish loop')
    while True:
        frame = stream.read(4000, exception_on_overflow=False)
        channel.basic_publish(exchange='sensor_audio', body='{"channels":1,"rate":16000,"data":%s}' % frame.hex(), routing_key='')


if __name__ == "__main__":
    usb = get_usb_mic_idx()
    while True:
        try:
            publish_audio(usb)
        except Exception as oops:
            print('ERROR', oops)
