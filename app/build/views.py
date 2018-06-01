import re
from . import build as app
from flask import request, render_template, redirect, url_for, jsonify
from models import Build, Environ, Project
from orator.exceptions.query import QueryException
from app.helper import make_response


@app.route('/record', methods=['POST'])
def record():
    name = request.form.get('name')
    try:
        image_id = Build.insert(
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
        project = Project.find_name_or_new(name)
        project.last_image_id = image_id
        project.save()
    except QueryException as e:
        return make_response('fail', 404, e.message)
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
def environs(project='basic'):
    if request.method == 'GET':
        return render_template('environ/detail.html', project=project)
    try:
        data = request.json
        Environ.where('parent_id', 0).delete()
        data = [{
            'name': project,
            'key': item.get('key'),
            'value': item.get('value'),
            'parent_id': 0,
            'project_id': 0
        } for item in data]
        Environ.insert(data)
    except QueryException as e:
        return make_response('fail', 500, e.args)
    return redirect(url_for('build.index'))


@app.route('/env_query/<string:project>')
def env_query(project=None):
    data = Environ.where('name', project).get().serialize()
    return jsonify(data)


@app.route('/test')
def test():
    result = Project.find_name_or_new('basic')
    print(type(result), '------------')
    return ''
