# builtin
import os
# external
import flask
import watchdog


# INITS

app = flask.Flask(__name__)


# FUNCTIONS

assets_dir = 'static/assets/'
output_dir = 'static/css/'

def build_css():
    import subprocess

    args = {
        'source': '{}main.scss'.format(assets_dir),
        'output': '{}main.css'.format(output_dir),
    }
    subprocess.call('''
        sassc -m {source} {output} -s compressed
        '''.format(**args),
        shell=True,
        preexec_fn=os.setsid,
        stdout=subprocess.PIPE
    )
    print('Built {}main.css'.format(output_dir))

def watch_css():
    # build css on changes
    from watchdog.events import FileSystemEventHandler
    class If_scss_changes (FileSystemEventHandler):
        def on_modified (self, event): build_css()

    # monitor for changes
    from watchdog.observers import Observer
    watch = Observer()
    watch.schedule(If_scss_changes(), assets_dir)
    watch.start()
    print('Watching {} for changes'.format(assets_dir))

    # make an intial build
    build_css()


# ROUTES

@app.route('/')
def index():
    return flask.send_from_directory('static/css', 'main.css')


if __name__ == '__main__':
    watch_css()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
    )
