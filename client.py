import flask
import requests


app_uri = '/client'
app_port = 5001
app_url = 'http://127.0.0.1:%s%s' % (app_port, app_uri)
mic_url = 'http://127.0.0.1:5000/mic'
app = flask.Flask(__name__)


@app.route(app_uri)
def default():
    try:
        print(flask.request.form)
        return 'got it thanks!'
    except Exception as exc:
        print(exc)
        return exc


def subscribe():
    try:
        response = requests.request('POST', mic_url, data={'action': 'subscribe', 'url': app_url})
        print(response.text)
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    subscribe()
    app.run(port=app_port)
