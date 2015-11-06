start with

    cd /home/css_server
    source venv/bin/active
    python main.py

relavent files

    /etc/init/gunicorn.conf
    /etc/nginx/sites-available/css_server
    /etc/nginx/sites-enabled/(symlink)css_server
