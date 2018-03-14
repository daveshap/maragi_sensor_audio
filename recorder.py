import pyaudio
from sys import getsizeof

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
print("recording...")
frames = []
 
while True:
    try:
        data = stream.read(chunk)
        frames.append(data)
        print(len(frames), getsizeof(frames))
        if len(frames) > depth:
            frames.pop(0)
    except keyboardinterrupt:
        # do nothing here
        # stop recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        exit(0)
