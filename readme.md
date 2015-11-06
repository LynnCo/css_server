developement startup

    cd /home/css_server
    source venv/bin/active
    python main.py
    # runs on port 5000

relavent files

    /etc/init/gunicorn.conf
    /etc/nginx/sites-available/css_server
    /etc/nginx/sites-enabled/(symlink)css_server

long running services

    # start
    gunicorn -D --bind=0.0.0.0:8000 main:app
    service nginx start

    # stop
    pkill gunicorn
    service nginx stop
