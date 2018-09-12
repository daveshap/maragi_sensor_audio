import time
import uuid
import requests
import threading
import pyaudio
import flask
import json


subscribers = []
app_port = 6000
app_uri = '/mic'
app = flask.Flask(__name__)
channels = 1                        # num audio channels
rate = 16000                        # 16khz sample rate
chunk = 4000                        # 250ms per audio chunk


def publish_audio(data):
    payload = {'time': str(time.time()),
               'uuid': str(uuid.uuid4()),
               'sensor': 'audio',
               'sample_rate': rate,
               'channels': channels,
               'sample_width': 16,
               'side': 'mono',
               'data': data.hex()}
    for url in subscribers:
        try:
            resp = requests.request(method='PUT', url=url, json=payload)
            print(resp.text)
        except Exception as exc:
            print('EXCEPTION', exc)


def audio_listener():
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True)
    print('audio stream is open')
    while True:
        frame = stream.read(chunk)
        threading.Thread(target=publish_audio(frame)).start()


@app.route(app_uri, methods=['POST'])
def default():
    request = flask.request
    payload = json.loads(request.data)
    print(payload)
    if request.method == 'POST':
        if payload['action'] == 'subscribe':
            if payload['url'] not in subscribers:
                subscribers.append(payload['url'])
                return json.dumps({'result': 'successfully added URL to subscribers list'})
            else:
                return json.dumps({'result': 'URL was already in subscribers list'})


if __name__ == "__main__":
    threading.Thread(target=audio_listener).start()
    app.run(port=app_port)
