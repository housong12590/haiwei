from . import build as app
from flask import request, render_template
from models import Build
from app import db
from sqlalchemy.exc import IntegrityError
from app.helper import make_response, parse_sql_error


@app.route('/', methods=['POST'])
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
    except IntegrityError as e:
        code, msg = parse_sql_error(e)
        return make_response('fail', code, msg)
    return make_response('success')


@app.route('/index')
def index():
    sql = "SELECT name,tag,branch,status,command,created_at FROM builds WHERE tag IN (SELECT max(tag) FROM builds GROUP BY name);"
    data = db.session.execute(sql)
    return render_template('build/index.html', data=data)
