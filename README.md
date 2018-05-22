# Microphone Microservice

General purpose microphone service that publishes audio above a certain threshold

## Input

Any computer microphone device compatible with PyAudio

## Output

Publishes raw audio to any service that registers "raw_audio" as an input

Field | Description
--- | ---
time | unix epoch
uuid | uuid v4 identifier for sample
type | 'raw_audio'
source | 'microphone service'
data | binary sample data as string

## Requirements

* directory service
* pyaudio
* audioop
* flask
* microphone input device
