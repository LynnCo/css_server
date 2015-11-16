developement startup

    cd /home/css_server
    source venv/bin/active
    python main.py
    # runs on port 5000

production startup / teardown

    gunicorn -D --error-logfile=static/log.txt --access-logfile=static/log.txt --bind=0.0.0.0:8000 main:app
    service nginx start

    pkill gunicorn
    service nginx stop


relavent files

    ln -sv /home/css_server/conf/nginx.conf /etc/nginx/sites-enabled/css_server.conf
