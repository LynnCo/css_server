import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.send_from_directory('.', 'main.py')

if __name__ == '__main__':
    app.run(
        port=5555,
        debug=False,
    )
