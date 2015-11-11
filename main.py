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


# log to STDOUT and static/log.txt
stream_handler = logging.StreamHandler()
file_handler = RotatingFileHandler('static/log.txt', maxBytes=10000)

# configure logger for the flask dev server
werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.addHandler(stream_handler)
werkzeug_log.addHandler(file_handler)

# configure logger for flask
app.logger.addHandler(stream_handler)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


class Builder(object):

    def __init__(self, assets_dir, output_dir):
        self.assets_dir = assets_dir
        self.output_dir = output_dir

    def compile_sass(self, *args, **kwargs):
        for sass_file_path in glob(self.assets_dir+'*.*'):
            filename = sass_file_path.split(self.assets_dir)[-1].split('.')[0]
            css_path = self.output_dir + filename + '.css'

            app.logger.info('Building \'{}\''.format(css_path))

            sass_args = {
                'source': '{}'.format(sass_file_path),
                'output': '{}'.format(css_path),
            }
            subprocess.call('''
                sassc -m {source} {output} -s compressed
                '''.format(**sass_args),
                shell=True,
                preexec_fn=os.setsid,
                stdout=subprocess.PIPE
            )
        app.logger.info('Completed Build')

    def start(self):
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        handler = FileSystemEventHandler()
        handler.on_modified = self.compile_sass

        watch = Observer()
        watch.schedule(handler, self.assets_dir, recursive=True)
        watch.start()
        app.logger.info('Watching \'{}\' for changes'.format(self.assets_dir))

@app.before_first_request
def activate_sass_watcher():
    builder = Builder('static/assets/', 'static/css/')
    builder.start()
    builder.compile_sass()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=True,
    )
