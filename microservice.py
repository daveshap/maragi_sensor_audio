import time
import uuid
import requests
import audioop
import pyaudio
import json


headers = {'Content-Type': 'application/octet-stream'}
directory = 'http://127.0.0.1:5000/directory'
channels = 1                        # num audio channels
rate = 16000                        # samples per second
chunk = 1024                        # samples per chunk
audio = pyaudio.PyAudio()           # audio device object
silence = 1                         # num seconds of silence to demarcate sounds
threshold = 2500                    # silence threshold TODO auto adapt to ambient noise
depth = int(rate / chunk * silence) # number of chunks to keep in memory


def publish_audio(frames, phonebook):
    data = b''.join(frames)
    t = time.time()
    u = uuid.uuid4()
    payload = {'time': str(t),
               'uuid': str(u),
               'type': 'raw_audio',
               'source': 'microphone service',
               'data': str(data)}
    for service in phonebook:
        try:
            if service['input'] == 'raw_audio':
                print('POST to', service)
                response = requests.request(method='PUT', url=service['svc_url'], json=payload)
                print(response)
        except Exception as exc:
            print(exc)


def record_sound(stream, sound_clip):
    tail_silence = 0
    print('recording audio')
    while True:
        frame = stream.read(chunk)
        sound_clip.append(frame)
        rms = audioop.rms(frame, 2)
        if rms < threshold:
            tail_silence += 1
        else:
            tail_silence = 0
        if tail_silence > depth:
            print('recording ended')
            return sound_clip


def get_phonebook():
    response = requests.request(method='GET', url=directory)
    text = response.text
    phonebook = json.loads(text)
    return phonebook


if __name__ == "__main__":
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
        elif len(sound_clip) < depth:
            continue
        if rms > threshold:
            audio_clip = record_sound(stream, sound_clip)
            phonebook = get_phonebook()
            publish_audio(audio_clip, phonebook)
            sound_clip = []
