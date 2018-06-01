#!/bin/sh

source venv/bin/activate
orator migrate -f -n -c config/pro_conf.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - manage:app
