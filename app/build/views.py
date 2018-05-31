import re
from . import build as app
from flask import request, render_template
from models import Build, Environ
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
            code_registry=request.form.get('code_registry'),
            message=request.form.get('message')
        )
    except QueryException as e:
        return make_response('fail', 404, e.args)
    return make_response('success')


@app.route('/index')
def index():
    data = Build.project_last_images().get()
    return render_template('build/index.html', data=data)


@app.route('/<project>/<tag>')
def detail(project, tag):
    data = Build.project_detail(project, tag).first()
    data.command = data.command.replace('\n', '<br/>')
    return render_template('build/detail.html', data=data)


@app.route('/<project>')
def images(project):
    data = Build.where('name', project).order_by('tag', 'desc').get()
    return render_template('build/images.html', data=data)


@app.route('/environs', methods=['GET', 'POST'])
@app.route('/environs/<string:project>', methods=['GET', 'POST'])
def env_detail(project=None):
    if project is None:
        sql = 'SELECT * FROM environs WHERE parent_id = 0'
    else:
        sql = 'SELECT * FROM environs AS e1 JOIN environs AS e2 ON e1.parent_id = e2.id WHERE e1.name=%s AND e1.parent_id=0'
    data = SQLHelper.fetch_all(sql, [project])
    print(data)
    if request.method == 'GET':
        return render_template('environ/detail.html', project='coasts')
    print(request.json)
    return ''


@app.route('/')
def basic_environs():
    pass
