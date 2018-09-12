# Microphone Microservice

Generic microphone publisher for MARAGI. Includes Dockerfile for composing Docker image. 

## Input

Any computer microphone device compatible with PyAudio.

## Docker

Make sure to instantiate your Docker container with `docker run --device /dev/snd:/dev/snd <container_name>`

## Output

Emits raw hexadecimal audio sample of size 4000 samples at rate of 16kHz. Thus each sample is 250ms. This is pretty standard for audio streaming in real-time for speech recognition and other sound detection.