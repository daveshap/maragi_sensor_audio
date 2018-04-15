import math
from collections import deque
import audioop
from flask import Flask, request
import time
import json
import threading
import pyaudio

#######################     flask stuff

subscribers = []

#######################     audio stuff

frames = []  # container for audio samples
channels = 1  # num audio channels
rate = 44100  # samples per second
chunk = 1024  # samples per chunk
audio = pyaudio.PyAudio()  # audio device object
depth = int(rate / chunk * 20)  # num seconds of audio to keep in memory
silence = 2  # num seconds of silence to demarcate sounds i.e. all sounds within 2 seconds are part of same phrase
threshold = 2500  # silence threshold


def thread_recorder():
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
    while True:
        try:
            frame = stream.read(chunk)
            frames.append(frame.hex())
            if len(frames) > depth:
                frames.pop(0)
        except Exception as exc:
            print(exc)
            pass


def post_sound(clip):
    print('posting clip to ???')


def thread_listener():
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
    while True:
        # wait for sound to start
        print('listening for sound...')
        audio2send = []
        rel = rate / chunk
        slid_win = deque(maxlen=silence * rel)
        prev_audio = deque(maxlen=silence * rel)  # Prepend audio from 0.5 seconds before noise was detected
        started = False
        cur_data = stream.read(chunk)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        if sum([x > threshold for x in slid_win]) > 0:
            print('sound detected, recording...')
            while True:
                audio2send.append(cur_data)
                started = False
                slid_win = deque(maxlen=silence * rel)
                prev_audio = deque(maxlen=0.5 * rel)
                audio2send = []
                tail_silence = 0
                if tail_silence > silence:
                    print('sound ended, sending now')
                    post_sound(audio2send)
                    break


app = Flask(__name__)


@app.route("/mic", methods=['GET', 'POST'])
def default():
    if request.method == 'GET':
        obj = {'payload': frames, 'time': time.time()}
        return json.dumps(obj)
    elif request.method == 'POST':
        post = request.form
        if post['action'] == 'subscribe':
            sub = (post['ip'], post['port'])
            if sub in subscribers:
                return 'already subscribed!'
            else:
                subscribers.append(sub)
                return 'subscribed'
        elif post['action'] == 'unsubscribe':
            sub = (post['ip'], post['port'])
            if sub in subscribers:
                subscribers.remove(sub)
                return 'unsubscribed'
            else:
                return 'not a subscriber'


if __name__ == "__main__":
    recorder = threading.Thread(target=thread_recorder)
    recorder.start()
    listener = threading.Thread(target=thread_listener)
    listener.start()
    app.run(port=5000, debug=True)
