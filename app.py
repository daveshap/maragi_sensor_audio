from flask import Flask
import time
import json
import threading
import pyaudio
import sys

frames = []


def thread_recorder():
    global frames
    frames = []
    format = pyaudio.paInt16
    channels = 1
    rate = 44100  # samples per second
    chunk = 1024  # samples per chunk
    audio = pyaudio.PyAudio()
    depth = int(rate / chunk * 20)
    # start recording
    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
    while True:
        try:
            data = stream.read(chunk)
            frames.append(data.hex())
            if len(frames) > depth:
                frames.pop(0)
        except Exception as exc:
            pass


app = Flask(__name__)


@app.route("/")
def default():
    obj = {'payload': frames,
           'time': time.time()}
    return json.dumps(obj)


if __name__ == "__main__":
    thread = threading.Thread(target=thread_recorder)
    thread.start()
    if sys.argv[1] is int:
        app.run(port = sys.argv[1])
    else:
        app.run(port=5000)
        
