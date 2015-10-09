# builtin
import os
# external
import flask
import watchdog


# INITS

app = flask.Flask(__name__)


# FUNCTIONS

def build_css():
    import subprocess

    args = {
        'source': 'assets/main.scss',
        'output': 'css/main.css',
    }
    subprocess.call('''
        sassc -m {source} {output} -s compressed
        '''.format(**args),
        shell=True,
        preexec_fn=os.setsid,
        stdout=subprocess.PIPE
    )
    print('Built CSS')

def watch_css():
    # build css on changes
    from watchdog.events import FileSystemEventHandler
    class If_scss_changes (FileSystemEventHandler):
        def on_modified (self, event): build_css()

    # monitor for changes
    from watchdog.observers import Observer
    watch = Observer()
    watch.schedule(If_scss_changes(), 'assets/')
    watch.start()
    print('Watching assets/ for changes')

    # make an intial build
    build_css()


# ROUTES

@app.route('/')
def index():
    return flask.send_from_directory('.', 'main.py')


if __name__ == '__main__':
    watch_css()
    app.run(
        port=5555,
        debug=False,
    )
