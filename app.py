import requests
import audioop
import flask
import time
import json
import threading
import pyaudio

#           flask stuff

subscribers = []    # list of urls to post sounds to
port = 5000         # this needs to be a system argument

#           audio stuff

frames = []                         # container for audio samples
channels = 1                        # num audio channels
rate = 44100                        # samples per second
chunk = 1024                        # samples per chunk
audio = pyaudio.PyAudio()           # audio device object
depth = int(rate / chunk * 20)      # num seconds of audio to keep in memory
silence = 2                         # num seconds of silence to demarcate sounds
threshold = 2500                    # silence threshold


def thread_recorder():
    print('recorder started')
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
    for sub in subscribers:
        try:
            response = requests.request('POST', sub, data={'time': time.time(), 'hex': clip})
            print('POST to', sub, response.status_code)
        except Exception as exc:
            print(exc)


def thread_listener():
    print('listener started')
    sound_clip = []
    depth = int(rate / chunk * silence)
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
    while True:
        frame = stream.read(chunk)
        sound_clip.append(frame.hex())
        rms = audioop.rms(frame, 2)
        print(rms)
        if len(sound_clip) > depth:
            sound_clip.pop(0)
        if rms > threshold:
            print('sound detected, recording...')
            audio2send = list()
            audio2send.append(sound_clip)
            tail_silence = 0
            frames_count = 0
            while True:
                frame = stream.read(chunk)
                audio2send.append(frame.hex())
                frames_count += 1
                rms = audioop.rms(frame, 2)
                if rms < threshold:
                    tail_silence += 1
                else:
                    tail_silence = 0
                if tail_silence > (rate / chunk * silence):
                    print('sound ended, sending now')
                    post_sound(audio2send)
                    break


app = flask.Flask(__name__)


@app.route("/mic", methods=['GET', 'POST'])
def default():
    
    if flask.request.method == 'GET':
        # returns current 'frames', which is last 20 seconds of raw audio
        obj = {'payload': frames, 'time': time.time()}
        return json.dumps(obj)

    elif flask.request.method == 'POST':
        # expects object {action: (un)subscribe, url: http://blah:#/blah}
        post = flask.request.form
        try:
            
            if post['action'] == 'subscribe':
                sub = post['url']
                if sub in subscribers:
                    return 'already subscribed!'
                else:
                    subscribers.append(sub)
                    return 'subscribed'
            
            elif post['action'] == 'unsubscribe':
                sub = post['url']
                if sub in subscribers:
                    subscribers.remove(sub)
                    return 'unsubscribed'
                else:
                    return 'not a subscriber'
        
        except Exception as exc:
            return str(exc)


if __name__ == "__main__":
    recorder = threading.Thread(target=thread_recorder)
    recorder.start()
    listener = threading.Thread(target=thread_listener)
    listener.start()
    app.run(port=port, debug=True)
