import re
from . import build as app
from flask import request, render_template, redirect, jsonify, json, url_for, abort
from models import Build, Environ, Project
from orator.exceptions.query import QueryException
from app.helper import make_response


@app.route('/record', methods=['POST'])
def record():
    name = request.form.get('name')
    try:
        project = Project.find_name_or_new(name)
        build = Build.create_new(request.form)
        project.last_image_id = build.id
        project.save()
    except QueryException as e:
        return make_response('fail', 500, e.message)
    return make_response('success')


@app.route('/delete_project/<int:project_id>')
def delete_project(project_id):
    project = Project.find_or_fail(project_id)
    name = project.name
    project.delete()
    Build.del_project(name)
    return redirect(url_for('build.projects'))


@app.route('/projects')
def projects():
    data = Project.all()
    return render_template('build/projects.html', data=data)


@app.route('/index')
def index():
    data = Build.project_last_images().get()
    return render_template('build/index.html', data=data)


@app.route('/images/<project>/<tag>')
def detail(project, tag):
    data = Build.project_detail(project, tag).first()
    data.command = data.command.replace('\n', '<br/>')
    return render_template('build/detail.html', data=data)


@app.route('/images/<project>')
def images(project):
    data = Build.where('name', project).order_by('tag', 'desc').get()
    return render_template('build/images.html', data=data)


@app.route('/global_environs', methods=['GET', 'POST'])
@app.route('/global_environs/<int:env_id>', methods=['GET', 'POST'])
def global_environs(env_id=None):
    env_obj = Environ.find(env_id)
    if request.method == 'GET':
        return render_template('environ/detail.html', env_id=env_obj)
    if env_obj is None:
        env_obj = Environ()
    try:
        env_dict = {item.get('key'): item.get('value') for item in request.json}
        env_obj.content = json.dumps(env_dict)
        env_obj.save()
    except QueryException:
        abort(404)
    return redirect(url_for('build.index'))


@app.route('/project_environs/<int:project_id>', methods=['GET', 'POST'])
def project_environs(project_id):
    if request.method == 'GET':
        return render_template('environ/detail.html', project_id=project_id)
    env_dict = {item.get('key'): item.get('value') for item in request.json}
    try:
        pro_obj = Project.find(project_id)

        if pro_obj.env_id == 0:
            env_obj = Environ()
        else:
            env_obj = Environ.find(pro_obj.env_id)
        env_obj.content = json.dumps(env_dict)
        env_obj.save()

        pro_obj.env_id = env_obj.id
        pro_obj.save()
    except QueryException:
        abort(404)
    return redirect(url_for('build.projects'))


@app.route('/query_env_environs/<int:env_id>')
@app.route('/query_project_environs/<int:project_id>')
def query_environs(env_id=None, project_id=None):
    if env_id:
        env = Environ.find(env_id).serialize()
        content = env.get('content')
        content = json.loads(content)
        data = [{'key': k, 'value': v} for k, v in content.items()]
        return jsonify(data)
    env = Environ.find(1).serialize()
    content = env.get('content')
    content = json.loads(content)
    project = Project.find(project_id)
    last_image = Build.find(project.last_image_id)
    env_exp = re.compile(r"-e (\w*?)='?(.*?)'? ")
    env_all = env_exp.findall(last_image.command)
    env_dict = dict(env_all)
    for k, v in env_dict.items():
        if content.get(k):
            env_dict[k] = content.get(k)
    data = [{'key': k, 'value': v} for k, v in env_dict.items()]
    return jsonify(data)


@app.route('/test/<project>')
def test(project):
    data = Environ.where('name', project).get().serialize()
    # last_image = Build.last_image(project)
    # env_exp = re.compile(r"-e (\w*?)='?(.*?)'? ")
    # env_all = env_exp.findall(last_image.command)
    # data = [{'key': env[0], 'value': env[1]} for env in env_all]
    return jsonify(data)
