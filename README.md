# microphone microservice

provides out-of-the-box functionality for robotics and ai in the form of a simple and robust rest api

## requirements

* json
* 
* sys
* flask

## usage

`python app.py <port (optional), default 5000>`

Endpoint | Function | Description | Example
--- | --- | --- | ---
/ | GET | Returns default dictionary | `{time: unix epoch, hex: 20 seconds of hex encoded samples }`
