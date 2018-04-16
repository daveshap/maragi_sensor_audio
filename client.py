import flask
import requests


url = 'http://127.0.0.1:5001/client'
app = flask.Flask(__name__)


@app.route("/client", methods=['GET', 'POST'])
def default():
    if flask.request.method == 'POST':
        print(flask.request.form)
        return 'got it thanks!'


def subscribe():
    try:
        response = requests.request('POST', 'http://127.0.0.1:5000/mic', data={'action': 'subscribe', 'url': url})
        print(response)
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    subscribe()
    app.run(port=5001)
