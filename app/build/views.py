from . import build as app
from flask import request, render_template, abort
from models import Build
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from app.helper import make_response, parse_sql_error
import re


@app.route('/record', methods=['POST'])
def record():
    try:
        build = Build(
            name=request.form.get('name'),
            tag=request.form.get('tag'),
            branch=request.form.get('branch'),
            status=request.form.get('status'),
            command=request.form.get('command')
        )
        build.command = re.sub(r'(-[vpe])', r'\\\n\1', build.command)
        db.session.add(build)
        db.session.commit()
    except IntegrityError as e:
        code, msg = parse_sql_error(e)
        return make_response('fail', code, msg)
    return make_response('success')


@app.route('/index')
def index():
    sql = "SELECT * FROM builds WHERE tag IN (SELECT max(tag) FROM builds GROUP BY name);"
    data = db.session.execute(sql)
    return render_template('build/index.html', data=data)


@app.route('/<project>/<tag>')
def detail(project, tag):
    try:
        data = db.session.query(Build).filter(Build.name == project) \
            .filter(Build.tag == tag).one()
        return render_template('build/detail.html', data=data)
    except NoResultFound:
        abort(404)


@app.route('/<project>')
def images(project):
    try:
        data = db.session.query(Build).filter(Build.name == project) \
            .order_by(Build.created_at).all()
        return render_template('build/images.html', data=data)
    except NoResultFound:
        abort(404)
