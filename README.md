# Microphone Microservice

Generic microphone publisher for MARAGI. Includes Dockerfile for composing Docker image. 

## Input

Any computer microphone device compatible with PyAudio.

## Docker

Instantiate the RabbitMQ container for the first time:
* `docker run -d --hostname maragi-rabbit --name maragi_rabbit -p 8080:15672 rabbitmq:3-management`

## Output

Emits raw hexadecimal audio sample of size 4000 samples at rate of 16kHz. Thus each sample is 250ms. This is pretty standard for audio streaming in real-time for speech recognition and other sound detection.