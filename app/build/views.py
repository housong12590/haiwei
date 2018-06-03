import json
from . import build as app
from flask import request, render_template, redirect, url_for
from models import Build, Environ, Project
from orator.exceptions.query import QueryException
from app.helper import make_response, list2dict, dict2list, get_environs


@app.route('/record', methods=['POST'])
def record():
    name = request.form.get('name')
    try:
        project = Project.find_name_or_new(name)
        build = Build.create_new(request.form)
        env_dict = get_environs(build.command)
        project.curr_tag = build.tag
        project.change = env_dict
        project.save()

    except QueryException as e:
        return make_response('fail', 500, e.message)
    return make_response('success')


@app.route('/projects')
def projects():
    project_list = Project.select(Project.raw('curr_tag')).get()
    tags = [pro.curr_tag for pro in project_list]
    data = Build.find_by_tags(tags).get()
    return render_template('build/project_index.html', data=data)


@app.route('/project_delete/<int:project_id>')
def project_delete(project_id):
    project = Project.find_or_fail(project_id)
    name = project.name
    project.delete()
    Build.find_by_name(name).delete()
    return redirect(url_for('build.projects'))


@app.route('/project_detail/<project_name>')
def project_detail(project_name):
    project = Project.find_by_name(project_name).first()
    build = Build.find_by_tag(project.curr_tag).first()
    count = Build.find_by_name(project.name).count()
    return render_template('build/project_detail.html', project=project, build=build, count=count)


@app.route('/images')
def image_all():
    data = Build.order_by('tag', 'desc').get()
    return render_template('build/image_list.html', data=data)


@app.route('/images/<name>')
def project_image(name):
    data = Build.find_by_name(name).order_by('tag', 'desc').get()
    return render_template('build/image_list.html', data=data)


@app.route('/image/<tag>')
def image_detail(tag):
    data = Build.find_by_tag(tag).first()
    data.command = data.command.replace('\n', '<br/>')
    return render_template('build/image_details.html', data=data)


@app.route('/environs/index')
def environs_index():
    data = Environ.all()
    return render_template('build/environ_index.html', data=data)


@app.route('/global_environs', methods=['GET', 'POST'])
@app.route('/global_environs/<int:eid>', methods=['GET', 'POST'])
def global_environs(eid=None):
    env_obj = Environ.find(eid)
    if request.method == 'GET':
        data = [{}]
        if env_obj:
            env_dict = json.loads(env_obj.value)
            data = dict2list(env_dict)
        return render_template('build/environ_global.html', data=data)
    if env_obj is None:
        env_obj = Environ()
    try:
        env_dict = list2dict(request.json)
        env_obj.value = json.dumps(env_dict, sort_keys=False)
        env_obj.default = True
        env_obj.save()
    except QueryException as e:
        return make_response('fail', 500, e.message)
    return make_response()


@app.route('/project_environs/<pid>', methods=['GET', 'POST'])
def project_environs(pid):
    pro_obj = Project.find_or_fail(pid)
    if request.method == 'GET':
        data = dict2list(pro_obj.environs)
        return render_template('build/environ_project.html', data=data)
    try:
        env_dict = list2dict(request.json)
        pro_obj.environs = env_dict
        pro_obj.change = env_dict
        pro_obj.save()
    except QueryException as e:
        return make_response('fail', 500, e.message)
    return make_response()
