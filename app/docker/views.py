from . import docker as app
from orator.exceptions.query import QueryException
from flask import request, render_template, redirect, url_for, abort, jsonify, flash
from app.helper import make_response
from models import Image, Deploy, User
from flask_login import current_user, login_required, login_user, logout_user
from config import Config
from app import db
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
    image_tags = Image.select(db.raw('max(image_tag) as tag')).group_by('image_name').get()
    projects = Config.projects(False)
    last_images = Image.where_in('image_tag', [image.tag for image in image_tags]).get()
    Deploy.select(db.raw('max(image_tag) as tag')).group_by('image_name').get()
    for project in projects:
        for image in last_images:
            if project.get('name') == image.image_name:
                project['image'] = image
                break
        else:
            project['image'] = {}
    return render_template('docker/index.html', projects=projects)


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


@app.route('/deploy/<image_name>', methods=['GET', 'POST'])
def deploy(image_name):
    projects = Config.projects()
    project = None
    for item in projects:
        if image_name == item.get('name'):
            project = item
            break
    if request.method == 'GET':
        return render_template('docker/deploy/index.html', project=project)
    tag = request.form.get('image_tag')
    remark = request.form.get('remark')
    if deploy_image(tag, **{'deploy_type': 'pro', 'remark': remark}):
        flash('部署请求发送成功')
    else:
        flash('部署请求发送失败')
    return redirect(url_for('docker.index'))


def deploy_image(tag, **kwargs):
    image = Image.where('image_tag', tag).first()
    if image is None:
        abort(404)
    obj = Deploy()
    obj.remark = kwargs.get('remark', '')
    obj.image_tag = tag
    deploy_type = kwargs.get('deploy_type', 'dev')
    if deploy_type == 'dev':
        obj.dev = 'Y'
    else:
        obj.pro = 'Y'
    obj.save()
    if deploy_type == 'dev':
        return send_deploy_request(obj)
    return send_deploy_request(obj)


@app.route('/query_image/<image_name>')
def query_image(image_name):
    _images = Image.where('image_name', image_name).where('git_branch', 'master').order_by(
        'image_tag', 'desc').limit(
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
