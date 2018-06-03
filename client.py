import flask
import json
import requests


directory_url = 'http://127.0.0.1:5000/directory'
app = flask.Flask(__name__)                                     # flask app
app_port = 9999                                                 # port for this service to run on
app_uri = '/test'                                               # uri endpoint
app_ip = '127.0.0.1'                                            # ip address of local machine
app_url = 'http://%s:%s%s' % (app_ip, app_port, app_uri)        # receiving url


@app.route(app_uri, methods=['PUT', 'GET'])
def default():
    print(json.loads(flask.request.data))
    return json.dumps({'result': 'got it!'})


if __name__ == '__main__':
    service = {'input': 'raw_audio',
               'svc_url': app_url}
    print('REGISTER', service)
    response = requests.request(method='PUT', url=directory_url, json=service)
    print('RESPONSE', response)
    app.run(port=app_port)
