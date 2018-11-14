from . import docker as app
from orator.exceptions.query import QueryException
from flask import request, render_template, redirect, url_for, abort, jsonify, flash
from app.helper import make_response
from models import Project, Image, Deploy, User
from flask_login import current_user, login_required, login_user, logout_user
from config import Config
import re
import os
import json


def read_projects():
    with open(Config.PROJECTS_PATH, 'r', encoding='utf8') as f:
        text = json.load(f)
        return text.get('data')


@app.route('/push', methods=['POST'])
def push():
    image_args = {
        'image_name': request.form.get('image_name'),
        'pull_address': request.form.get('pull_address'),
        'image_tag': request.form.get('image_tag'),
        'git_branch': request.form.get('git_branch'),
        'git_message': request.form.get('git_message'),
        'code_registry': request.form.get('code_registry'),
        'host': request.form.get('host'),
        'port': request.form.get('port'),
        'command': re.sub(r'(-[vpe])', r'\\\n\1', request.form.get('command')),
        'dockerfile': request.form.get('dockerfile')
    }
    try:
        Image.insert(image_args)
    except QueryException as e:
        return make_response(e.message, status_code=500)
    return make_response()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.where('username', username).first()
    if user is None:
        flash('当前用户不存在,请联系管理员!')
        return render_template('login.html', username=username, password=password)
    if user.password != password:
        flash('登录密码错误!')
        return render_template('login.html', username=username, password=password)
    login_user(user)
    return redirect(url_for('docker.index'))


@login_required
@app.route('/')
def index():
    projects = Config.projects(False)
    return jsonify(projects)
    # projects = Project.all()
    # for project in projects:
    #     last_image = Image.where('image_name', project.image_name) \
    #         .order_by('image_tag', 'desc').first()
    #     project.image = last_image
    # image_names = Image.group_by('image_name').lists('image_name')
    # return render_template('docker/index.html', projects=projects, image_names=image_names)


@app.route('/project/<project_id>', methods=['GET', 'POST'])
@app.route('/project/create', methods=['GET', 'POST'])
def create_project(project_id=None):
    if request.method == 'GET':
        projects = None
        if project_id is None:
            data_dict = Config.projects()
            all_names = [k for k, v in data_dict.items()]
            exist_project = Project.where_in('name', all_names).get()
            exist_names = [project.name for project in exist_project]
            diff_names = set(all_names) - set(exist_names)
            projects = [data_dict.get(name) for name in diff_names]
        project = None
        image_names = Image.group_by('image_name').lists('image_name')
        if project_id:
            project = Project.find(project_id)
        return render_template('docker/project/create.html',
                               project=project,
                               image_names=image_names,
                               projects=projects)
    image_name = request.form.get('image_name', None)
    project_name = request.form.get('project_name', None)
    _auto_deploy = bool(request.form.get('auto_deploy'))
    try:
        if project_id is None:
            project_desc = ''
            for item in read_projects():
                if item.get('name') == project_name:
                    project_desc = item.get('description', '')
                    break
            if image_name and project_name:
                Project.insert({
                    'name': project_name,
                    'desc': project_desc,
                    'image_name': image_name,
                    'auto_deploy': _auto_deploy
                })
            else:
                return 'miss required parameter'
        else:
            project = Project.find(project_id)
            project.image_name = image_name
            project.auto_deploy = _auto_deploy
            project.save()
    except QueryException as e:
        return '' + str(e.args)
    return redirect(url_for('docker.index'))


@app.route('/delete_project/<project_id>')
def delete_project(project_id):
    project = Project.find_or_fail(project_id)
    project.delete()
    return redirect(url_for('docker.index'))


@app.route('/update')
def update():
    import requests
    from config import Config
    try:
        resp = requests.get(Config.PROJECT_LIST)
        if resp.status_code == 200:
            data = json.loads(resp.text, encoding='utf8')
            if data.get('status_code') == 200:
                file_path = os.path.abspath(Config.PROJECTS_PATH)
                with open(file_path, 'w', encoding='utf8')as f:
                    text = json.dumps(data, ensure_ascii=False)
                    f.write(text)
    except Exception as e:
        return "update fail \n %s" % e.args
    return jsonify(Config.projects(True))


@app.route('/images/<image_name>')
@app.route('/images')
def images(image_name=None):
    image = Image
    if image_name:
        image = image.where('image_name', image_name)
    data = image.order_by('image_tag', 'desc').get()
    return render_template('docker/images.html', images=data)


@app.route('deploy_history')
def deploy_history():
    deploys = Deploy.order_by('created_at', 'desc').get()
    return render_template('docker/deploy/history.html', deploys=deploys)


@app.route('/deploy/<project_id>', methods=['GET', 'POST'])
def deploy(project_id):
    project = Project.find(project_id)
    if project is None:
        abort(404)
    if request.method == 'GET':
        _images = Image.where('image_name', project.image_name).order_by('image_tag', 'desc').limit(
            10).get()
        return render_template('docker/deploy/index.html', images=_images, project=project)
    remark = request.form.get('remark')
    image_tag = request.form.get('image_tag')
    deploy_type = request.form.get('deploy_type')
    image = Image.where('image_tag', image_tag).first()
    print(request.form)
    if image is None:
        abort(404)
    _deploy = Deploy()
    _deploy.project_id = project.id
    _deploy.image_tag = image_tag
    _deploy.remark = remark
    if deploy_type == 'dev':
        _deploy.dev = 'Y'
    else:
        _deploy.pro = 'Y'
    try:
        _deploy.save()
        if deploy_type == 'dev':
            result = send_deploy_request(_deploy)
            print(result)
        else:
            send_wx_template_msg(_deploy)
    except QueryException as e:
        return str(e.args)
    return redirect(url_for('docker.index'))


@app.route('/query_image/<image_name>')
def query_image(image_name):
    _images = Image.where('image_name', image_name).order_by('image_tag', 'desc').limit(
        10).get()
    from app.helper import utc2local
    for image in _images:
        created_at = utc2local(image.created_at)
        image.created_at = None
        image.created_time = created_at
        image.updated_at = None
        image.code_registry = None
        image.dockerfile = None
        image.command = None
    _images = _images.to_json()
    _images = json.loads(_images, encoding='utf8')
    return jsonify(_images)


def auto_deploy():
    pass


def send_wx_template_msg(_deploy):
    pass


def send_deploy_request(_deploy):
    if _deploy is None:
        abort(500)
    project = Project.find(_deploy.project_id)
    if project is None:
        abort(500)
    image = Image.where('image_tag', _deploy.image_tag).first()
    if image is None:
        abort(500)
    print(image)
    image_address = image.pull_address.replace('192.168.0.210', 'registry.jiankanghao.net')
    import requests
    params = {
        'deployment_name': project.name,
        'image': image_address
    }
    if _deploy.dev == 'Y':
        base_url = Config.DEPLOY_DEV_URL
    else:
        base_url = Config.DEPLOY_PRO_URL
    resp = requests.post(base_url, params)
    if resp.status_code == 200:
        return True
    print(resp.text)
    return False
