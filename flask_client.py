import flask
import json
import requests


app = flask.Flask(__name__)                                     # flask app
app_port = 9999                                                 # port for this service to run on
app_uri = '/test'                                               # uri endpoint
app_ip = '127.0.0.1'                                            # ip address of local machine
app_url = 'http://%s:%s%s' % (app_ip, app_port, app_uri)        # receiving url
mic_url = 'http://127.0.0.1:6000/mic'


@app.route(app_uri, methods=['PUT', 'GET'])
def default():
    print(json.loads(flask.request.data))
    return json.dumps({'result': 'audio client successfully received'})


if __name__ == '__main__':
    response = requests.request(method='POST', url=mic_url, json={'action': 'subscribe', 'url': app_url})
    print('RESPONSE', response)
    app.run(port=app_port)
