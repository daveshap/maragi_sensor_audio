import pyaudio


frames = []                         # container for audio samples
channels = 1                        # num audio channels
rate = 16000                        # samples per second
chunk = 1024                        # samples per chunk
audio = pyaudio.PyAudio()           # audio device object


stream = audio.open(format=pyaudio.paInt16,channels=channels,rate=rate,input=True,frames_per_buffer=chunk)

while True:
    frame = stream.read(chunk)
    print(frame.hex())
    exit()