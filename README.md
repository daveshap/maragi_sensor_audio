# Microphone Microservice

[MARAGI](https://github.com/benjaminharper2/maragi) microservice to provide audio clips for other services such as speech recognition and NLP

## Input

Any computer microphone

## Output

Serialized list of frames of audio samples compatible with PyAudio

## Requirements

* python3
* flask
* time
* json
* sys
* threading
* pyaudio

## API

Endpoint | Method | Request | Response
--- | --- | --- | ---
/ | GET | Returns default dictionary | `{time: unix epoch, hex: 20 seconds of hex encoded samples }`

