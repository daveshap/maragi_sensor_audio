import time
import uuid
import requests
import threading
import pyaudio
import json


directory = 'http://127.0.0.1:5000/directory'
phonebook = []
channels = 1                        # num audio channels
rate = 16000                        # 16khz sample rate
chunk = 4000                        # 250ms per audio chunk


def publish_audio(data):
    payload = {'time': str(time.time()),
               'uuid': str(uuid.uuid4()),
               'sensor': 'audio',
               'metadata': {'chunk': chunk,
                            'rate': rate,
                            'channels': channels,
                            'format': 'pyaudio.paInt16',
                            'encoding': 'hex'},
               'data': data.hex()}
    for service in phonebook:
        try:
            if service['input'] == 'audio':
                requests.request(method='PUT', url=service['svc_url'], json=payload)
        except Exception as exc:
            print(service, exc)


def get_phonebook():
    # periodically updates the phonebook
    global phonebook
    while True:
        response = requests.request(method='GET', url=directory)
        text = response.text
        phonebook = json.loads(text)
        print('PHONEBOOK UPDATED', phonebook)
        time.sleep(60)


if __name__ == "__main__":
    phonebook_updater = threading.Thread(target=get_phonebook)
    phonebook_updater.start()
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                    channels=channels,
                                    rate=rate,
                                    input=True)
    print('audio stream is open')
    while True:
        frame = stream.read(chunk)
        publisher = threading.Thread(target=publish_audio(frame))
        publisher.start()
