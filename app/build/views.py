import re
from . import build as app
from flask import request, render_template
from models import Build
from orator.exceptions.query import QueryException
from app.helper import make_response
from app.utils.db_helper import SQLHelper


@app.route('/record', methods=['POST'])
def record():
    try:
        Build.insert(
            name=request.form.get('name'),
            tag=request.form.get('tag'),
            status=bool(request.form.get('status')),
            branch=request.form.get('branch'),
            host=request.form.get('host'),
            port=request.form.get('port'),
            notify=request.form.get('notify'),
            command=re.sub(r'(-[vpe])', r'\\\n\1', request.form.get('command')),
            image_name=request.form.get('image_name'),
            send=bool(request.form.get('send')),
            dockerfile=request.form.get('dockerfile'),
            code_registry=request.form.get('code_registry')
        )
    except QueryException as e:
        return make_response('fail', 404, e.args)
    return make_response('success')


@app.route('/index')
def index():
    sql = "SELECT name,tag,branch,host,created_at,command FROM builds WHERE tag IN (SELECT max(tag) FROM builds GROUP BY name)"
    data = SQLHelper.fetch_all(sql)
    return render_template('build/index.html', data=data)


@app.route('/<project>/<tag>')
def detail(project, tag):
    data = SQLHelper.fetch_one("SELECT * FROM builds WHERE name=%s AND tag=%s", [project, tag])
    data['command'] = data['command'].replace('\n', '<br/>')
    return render_template('build/detail.html', data=data)


@app.route('/<project>')
def images(project):
    sql = "SELECT name,tag,branch,host,command,created_at FROM builds WHERE name=%s ORDER BY tag DESC"
    data = SQLHelper.fetch_all(sql, [project])
    return render_template('build/images.html', data=data)
