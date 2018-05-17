from . import build as app
from flask import request, render_template
from models import Build
from app import db
from sqlalchemy.exc import IntegrityError
from app.helper import make_response, parse_sql_error


@app.route('/record', methods=['GET', 'POST'])
def record():
    try:
        build = Build(
            name=request.form.get('name'),
            tag=request.form.get('tag'),
            branch=request.form.get('branch'),
            status=request.form.get('status'),
            command=request.form.get('command')
        )
        db.session.add(build)
        db.session.commit()
        return make_response('success')
    except IntegrityError as e:
        code, msg = parse_sql_error(e.args)
        return make_response(msg, code)


@app.route('/index')
def index():
    data = db.session.query(Build).all()
    return render_template('build/index.html', data=data)
