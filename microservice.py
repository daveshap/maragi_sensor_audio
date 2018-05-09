import requests
import audioop
import flask
import threading
import pyaudio

#                                   flask stuff
subscribers = []                    # list of urls to post sounds to
app_port = 5000                     # this needs to be a system argument  TODO optional argument
app_uri = '/mic'                    # api endpoint  TODO optional argument
app = flask.Flask(__name__)         # flask app
headers = {'Content-Type': 'application/octet-stream'}

#                                   audio stuff
channels = 1                        # num audio channels
rate = 16000                        # samples per second
chunk = 1024                        # samples per chunk
audio = pyaudio.PyAudio()           # audio device object
silence = 1                         # num seconds of silence to demarcate sounds
threshold = 2500                    # silence threshold  TODO auto adapt to ambient noise
depth = int(rate / chunk * silence) # number of chunks to keep in memory


def send_to_subscribers(frames):
    data = b''.join(frames)
    for sub in subscribers:
        try:
            response = requests.request(method='POST', url=sub, data=data, headers=headers)
            print('POST to', sub, response.text)
        except Exception as exc:
            print('EXCEPTION', exc)


def start_recording(stream, sound_clip):
    tail_silence = 0
    while True:
        frame = stream.read(chunk)
        sound_clip.append(frame)
        rms = audioop.rms(frame, 2)
        if rms < threshold:
            tail_silence += 1
        else:
            tail_silence = 0
        if tail_silence > depth:
            print('sound ended, sending now')
            send_to_subscribers(sound_clip)
            return


def listener():
    print('listener started')
    sound_clip = []
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
    while True:
        frame = stream.read(chunk)
        sound_clip.append(frame)
        rms = audioop.rms(frame, 2)
        if len(sound_clip) > depth:
            sound_clip.pop(0)
        if rms > threshold:
            print('sound detected, recording...')
            start_recording(stream, sound_clip)


@app.route(app_uri, methods=['POST'])
def default():
    try:
        post = flask.request.form
        print('POST received', post)
        sub = post['url']
        if post['action'] == 'subscribe':
            if sub in subscribers:
                return 'subscribed'
            subscribers.append(sub)
            return 'subscribed'
        elif post['action'] == 'unsubscribe':
            subscribers.remove(sub)
            return 'unsubscribed'
    except Exception as exc:
        print('EXCEPTION', exc)
        return exc


if __name__ == "__main__":
    thread = threading.Thread(target=listener)
    thread.start()
    app.run(port=app_port)
