# builtin
import os
from glob import glob
import logging
from logging.handlers import RotatingFileHandler

# external
import flask
import watchdog
import subprocess
from dotenv import load_dotenv


load_dotenv('.env')
app = flask.Flask(__name__)


# do I really need this many lines for logging?
handler = RotatingFileHandler('static/log.txt', maxBytes=10000, backupCount=1)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
routeLogger = logging.getLogger('werkzeug')
routeLogger.addHandler(handler)
routeLogger.setLevel(logging.INFO)


assets_dir = 'static/assets/'
output_dir = 'static/css/'


def build_css():
    for sass_path in glob(assets_dir+'*.*'):
        filename = sass_path.split(assets_dir)[-1].split('.')[0]
        css_path = output_dir + filename + '.css'

        app.logger.info('Building {}'.format(css_path))

        args = {
            'source': '{}'.format(sass_path),
            'output': '{}'.format(css_path),
        }
        subprocess.call('''
            sassc -m {source} {output} -s compressed
            '''.format(**args),
            shell=True,
            preexec_fn=os.setsid,
            stdout=subprocess.PIPE
        )
    app.logger.info('Completed Build')

def watch_css():
    # build css on changes
    from watchdog.events import FileSystemEventHandler
    class If_sass_changes (FileSystemEventHandler):
        def on_modified (self, event): build_css()

    # monitor for changes
    from watchdog.observers import Observer
    watch = Observer()
    watch.schedule(If_sass_changes(), assets_dir, recursive=True)
    watch.start()
    app.logger.info('Watching {} for changes'.format(assets_dir))

    # make an intial build
    build_css()


if __name__ == '__main__':
    watch_css()
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=False,
    )
