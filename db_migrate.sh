#!/usr/bin/env bash

python manage.py db init
python manage.py db migrate -m "initial migration"
python manage.py db upgrade