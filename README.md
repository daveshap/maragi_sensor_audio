# Microphone Microservice

Generic microphone publisher for MARAGI. Includes Dockerfile for composing Docker image. 

## Input

Any computer microphone device compatible with PyAudio.

## Docker

This is meant to run with [maragi_rabbit](https://hub.docker.com/r/daveshap/maragi_rabbit/)

## Output

Emits raw hexadecimal audio sample of size 4000 samples at rate of 16kHz. Thus each sample is 250ms. This is pretty standard for audio streaming in real-time for speech recognition and other sound detection.