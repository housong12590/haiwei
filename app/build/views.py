from . import build as app
from flask import request, render_template
from models import Build
from app import db
from app import mongo
from sqlalchemy.exc import IntegrityError
from app.helper import make_response, parse_sql_error
import time


@app.route('/record', methods=['GET', 'POST'])
def record():
    build = {
        'name': request.form.get('name'),
        'tag': request.form.get('tag'),
        'branch': request.form.get('branch'),
        'status': request.form.get('status'),
        'created_at': time.strftime("%Y-%m-%d %H:%M:%S"),
        'command': request.form.get('command')
    }
    print(request.form)
    if 'hous' in request.form:
        print('-------------')
    mongo.db.build.insert_one(build)
    return make_response('success')


@app.route('/index')
def index():
    # data = db.session.query(Build).all()
    # return render_template('build/index.html', data=data)
    # users = mongo.db.users.find()
    data = mongo.db.build.find()
    return render_template('build/index.html', data=data)
