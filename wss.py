import pyaudio
import websocket
import pickle


#record
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 40

HOST = 'ws://127.0.0.1:8080'

s = websocket.create_connection(HOST)

s.send('Hii')

p = pyaudio.PyAudio()

for i in range(0, p.get_device_count()):
    print(i, p.get_device_info_by_index(i)['name'])

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=1)

print("*recording")

i = 0
frames = []

while i < 20:
    data  = stream.read(CHUNK)
    frames.append(data)
    print(i)
    i += 1

s.send(pickle.dumps(frames))