#!/bin/sh

source venv/bin/activate
orator migrate -f -n -c db_conf.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - pro:app
