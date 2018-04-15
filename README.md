# Microphone Microservice

[MARAGI](https://github.com/benjaminharper2/maragi) microservice to provide audio clips for other services such as speech recognition and NLP.
Allows services to subscribe. This service will POST detected sounds to given URL (IP or hostname, port, API endpoint).

## Input

Any computer microphone device

## Output

Serialized list of frames of audio samples compatible with PyAudio

## Requirements

* python3
* flask
* time
* json
* threading
* pyaudio
* collections
* audioop

## API

Endpoint | Method | Request | Response
--- | --- | --- | ---
/mic | GET | `''` | `{time: unix epoch, hex: 20 seconds of hex encoded samples }`
/mic | POST | subscribe or unsubscribe `{action: (un)subscribe, url: http://blah:9999/api/endpoint}` | acknowledgement of subscription status, subscription messages same format as GET response

