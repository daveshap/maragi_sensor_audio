import pyaudio
import pika


def get_usb_mic_idx(audio):
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if 'USB' in info['name'] and 'Audio' in info['name']:
            print('FOUND audio device', info)
            return i
    exit('No USB audio devices detected. Please run container with --privileged')


def publish_audio_loop(stream, channel):
    print('starting publish loop')
    while True:
        frame = stream.read(4000, exception_on_overflow=False)
        channel.basic_publish(exchange='sensor_audio', body='{"channels":1,"rate":16000,"data":%s}' % frame.hex(), routing_key='')


def open_amqp_conn():        
    print('opening AMQP connection')
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    return channel


if __name__ == "__main__":
    while True:
        try:
            audio = pyaudio.PyAudio()
            usb = get_usb_mic_idx(audio)
            print('opening audio stream')
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, input_device_index=usb)
            amqp = open_amqp_conn()
            publish_audio_loop(stream, amqp)
        except Exception as oops:
            audio.terminate()
            print('ERROR', oops)
