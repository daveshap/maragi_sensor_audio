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
audio = pyaudio.PyAudio()           # audio device object


def publish_audio(data):
    global phonebook
    t = time.time()
    u = uuid.uuid4()
    payload = {'time': str(t),
               'uuid': str(u),
               'type': 'raw_audio',
               'source': 'microphone service',
               'data': data}
    for service in phonebook:
        try:
            if service['input'] == 'raw_audio':
                #print('POST to', service)
                response = requests.request(method='PUT', url=service['svc_url'], json=payload)
                #print(response)
        except Exception as exc:
            print(exc)


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
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
    print('audio stream running')
    while True:
        frame = stream.read(chunk)
        publisher = threading.Thread(target=publish_audio(frame.hex()))
        publisher.start()
