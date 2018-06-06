import json
from . import build as app
from flask import request, render_template, redirect, url_for
from models import Build, Environ, Project, Image
from orator.exceptions.query import QueryException
from app.helper import make_response, list2dict, dict2list, get_environs
from flask_paginate import Pagination, get_page_parameter
import requests

per_page = 15


@app.route('/record', methods=['POST'])
def record():
    name = request.form.get('name')
    try:
        build = Build.create_new(request.form)
        project = Project.find_by_image_name(name)
        if project:
            project.last_tag = build.id
            project.save()
    except QueryException as e:
        return make_response('fail', 500, e.message)
    return make_response('success')


@app.route('/pull')
def pull():
    result = requests.get('http://192.168.0.240:30016/')
    if result.status_code == 200:
        data = json.loads(result.text, encoding='utf8')
        project_data = []
        for k, v in data.items():
            project = Project.find(k)
            if project is None:
                project = Project()
            project.id = k
            project.name = v.get('name')
            project.desc = v.get('desc')
            project.save()
        Project.insert(project_data)
    return redirect(url_for('build.projects'))


@app.route('/projects')
def projects():
    data = Project.all()
    for item in data:
        image_tag = item.last_tag
        item.image = Image.find_by_tag(image_tag)
    return render_template('build/project_index.html', projects=data)


@app.route('/project_delete/<project_id>')
def project_delete(project_id):
    project = Project.find(project_id)
    image_name = project.image_name
    Image.find_by_name(image_name).delete()
    project.delete()
    return redirect(url_for('build.projects'))


@app.route('/project_detail/<project_id>')
def project_detail(project_id):
    project = Project.find(project_id)
    image = Image.find_last_image(project.image_name)
    project.image = image
    return render_template('build/project_detail.html', project=project)


@app.route('/images')
def image_all():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page=per_page, total=Build.count(), bs_version=3)
    data = Build.order_by('tag', 'desc').paginate(per_page, page)
    return render_template('build/image_list.html', data=data, pagination=pagination)


@app.route('/images/<name>')
def project_image(name):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    data = Build.find_by_name(name)
    pagination = Pagination(page=page, per_page=per_page, total=data.count(), bs_version=3)
    data = data.order_by('tag', 'desc').paginate(per_page, page)
    return render_template('build/image_list.html', data=data, pagination=pagination)


@app.route('/image/<tag>')
def image_detail(tag):
    data = Build.find_by_tag(tag).first()
    data.command = data.command.replace('\n', '<br/>')
    return render_template('build/image_details.html', data=data)


@app.route('/environs/index')
def environs_index():
    data = Environ.first()
    # return render_template('build/environ_index.html', data=data)
    data = json.loads(data.value)
    return render_template('build/environ_index1.html', data=data)


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


@app.route('/project_environs/<name>', methods=['GET', 'POST'])
def project_environs(name):
    pro_obj = Project.find_by_name(name).first()
    if request.method == 'GET':
        data = dict2list(pro_obj.environs)
        return render_template('build/environ_project.html', project=pro_obj, data=data)
    try:
        env_dict = list2dict(request.json)
        pro_obj.environs = env_dict
        pro_obj.change = env_dict
        pro_obj.save()
    except QueryException as e:
        return make_response('fail', 500, e.message)
    return make_response()
