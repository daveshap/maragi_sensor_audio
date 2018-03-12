import pyaudio
from flask import Flask
import json

# global overhead stuff
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
audio = pyaudio.PyAudio()
frames = []
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)


def grab_sound_block(data):
    return frames 


app = Flask(__name__)

@app.route("/")
def default():
    return grab_sound_block(frames)


def record_loop(loop_on):
    while True:
        if loop_on.value == True:
            data = stream.read(CHUNK)
            frames.append(data)
        #time.sleep(1)


if __name__ == "__main__":
   recording_on = Value('b', True)
   p = Process(target=record_loop, args=(recording_on,))
   p.start()  
   app.run(debug=True,
           use_reloader=False,
           host='0.0.0.0',
           port=5000)
   p.join()
