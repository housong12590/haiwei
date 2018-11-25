from . import docker as app
from orator.exceptions.query import QueryException
from flask import request, render_template, redirect, url_for, abort, jsonify, flash
from app.helper import make_response
from models import Image, Deploy, Project, User
from flask_login import login_required, current_user
from flask_paginate import get_page_parameter, Pagination
from config import Config
from app.utils.msg import Ding
import re
import json


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
        if image_args.get('git_branch') == 'master':
            project = Project.where('image_name', image_args.get('image_name')).first()
            if project:
                project.new_tag = image_args.get('image_tag')
                project.save()
        else:
            deploy_image(image_args.get('image_tag'))
    except QueryException as e:
        return make_response(e.message, status_code=500)
    return make_response()


@app.route('/init')
def init():
    admin = User.where('is_admin', True).first()
    if admin is None:
        User.insert({'username': 'admin', 'nickname': '管理员', 'password': 'kexin123456', 'is_admin': True})
    import requests
    from config import Config
    resp = requests.get(Config.PROJECT_LIST)
    if resp.status_code == 200:
        data = json.loads(resp.text, encoding='utf8')
        if data.get('status_code') == 200:
            for item in data.get('data'):
                project = Project.where('name', item.get('name')).first()
                if project is None:
                    project = Project()
                image = item.get('image')
                try:
                    image, _ = image.split(':')
                except ValueError:
                    pass
                try:
                    prefix, image = image.rsplit('/', 1)
                except ValueError:
                    prefix = ''
                desc = item.get('description', '')
                find_index = desc.find('（')
                if find_index != -1:
                    desc = desc[:find_index]
                new_tag = Image.where('image_name', image).where('git_branch', 'master').max(
                    'image_tag')
                last_tag = Deploy.where('image_name', image).max('image_tag')
                project.name = item.get('name')
                project.image_name = image
                project.new_tag = new_tag
                project.last_tag = last_tag
                project.image_prefix = prefix
                project.desc = desc
                project.save()
    return redirect(url_for('docker.index'))


@app.route('/')
@login_required
def index():
    projects = Project.all()
    last_image_tags = [obj.new_tag for obj in projects if obj.new_tag]
    last_images = Image.where_in('image_tag', last_image_tags).get()
    for project in projects:
        for image in last_images:
            if project.image_name == image.image_name:
                project.image = image
                break
        else:
            project.image = None
    return render_template('docker/index.html', projects=projects)


@app.route('/images')
@login_required
def images():
    image = Image
    image_name = request.args.get('image_name')
    if image_name:
        image = image.where('image_name', image_name)
    data = image.order_by('image_tag', 'desc')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page=15, css_framework='foundation', total=data.count())
    data = data.paginate(15, page)
    return render_template('docker/images.html', images=data, pagination=pagination)


@app.route('deploy_history')
@login_required
def deploy_history():
    deploys = Deploy.join('projects', 'projects.image_name', '=', 'deploys.image_name') \
        .join('users', 'users.id', '=', 'deploys.user_id').order_by('deploys.created_at', 'desc')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page=15, css_framework='foundation', total=deploys.count())
    deploys = deploys.paginate(15, page)
    return render_template('deploy/history.html', deploys=deploys, pagination=pagination)


@app.route('/deploy/<image_name>', methods=['GET', 'POST'])
@login_required
def deploy(image_name):
    if request.method == 'GET':
        project = Project.where('image_name', image_name).first()
        last_deploy = Deploy.where('image_name', image_name).where('pro', 'N') \
            .order_by('created_at', 'desc').first()
        return render_template('deploy/index.html', project=project, deploy=last_deploy)
    tag = request.form.get('image_tag')
    remark = request.form.get('remark')
    if deploy_image(tag, remark):
        flash('部署请求发送成功')
    else:
        flash('部署请求发送失败')
    return redirect(url_for('docker.index'))


def deploy_image(tag, remark='开发环境部署', _type='dev'):
    image = Image.where('image_tag', tag).first()
    if image is None:
        abort(404)
    obj = Deploy()
    obj.image_tag = tag
    obj.image_name = image.image_name
    obj.remark = remark
    obj.type = _type
    obj.user_id = current_user.id
    obj.save()
    if _type == 'dev':
        return send_deploy_request(obj)
    return send_wx_template_msg(obj)


@app.route('/query_image/<image_name>')
@login_required
def query_image(image_name):
    _images = Image.where('image_name', image_name).where('git_branch', 'master').order_by(
        'image_tag', 'desc').limit(10).get()
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


def send_wx_template_msg(_deploy):
    change_deploy_status(_deploy, 'D')
    from app.utils import wx
    user = User.find(_deploy.user_id)
    project = Project.where('image_name', _deploy.image_name).first()
    wx.send_template_msg('', '', '', '', '', _deploy.remark)


@app.route('/verify_deploy/<deploy_id>', methods=['GET', 'POST'])
def verify_deploy(deploy_id):
    _deploy = Deploy.find(deploy_id)
    if _deploy is None:
        abort(500)
    if request.method == 'GET':
        image = Image.where('image_tag', _deploy.image_tag).first()
        project = Project.where('image_name', _deploy.image_name).first()
        user = User.find(_deploy.user_id)
        return render_template('deploy/verify.html', deploy=_deploy, image=image, project=project, user=user)
    admin_pwd = request.form.get('admin_pwd')
    admin = User.where('is_admin', True).first()
    if admin.password == admin_pwd:
        send_deploy_request(_deploy)
        flash('请求发送成功')
        return redirect(url_for('docker.index'))
    flash('密码错误!')
    return redirect(url_for('docker.verify_deploy', deploy_id=deploy_id))


def send_deploy_request(_deploy):
    if _deploy is None:
        abort(500)
    project = Project.where('image_name', _deploy.image_name).first()
    prefix = project.image_prefix
    image_name = _deploy.image_name
    image = '%s/%s:%s' % (prefix, image_name, _deploy.image_tag)
    import requests
    params = {
        'deployment_name': project.name,
        'image': image
    }
    if _deploy.type == 'dev':
        base_url = Config.DEPLOY_DEV_URL
    else:
        base_url = Config.DEPLOY_PRO_URL
    resp = requests.post(base_url, params)
    if resp.status_code == 200:
        if _deploy.type == 'pro':
            project = Project.where('image_name', _deploy.image_name).first()
            project.last_tag = _deploy.image_tag
            project.save()
        change_deploy_status(_deploy, 'Y')
        return True
    print(resp.text)
    change_deploy_status(_deploy, 'F')
    return False


def change_deploy_status(obj, status):
    msg = ''

    if obj.type == 'dev':
        obj.dev = status
        if status == 'Y':
            msg = obj.image_name + ':' + obj.image_tag + ' 管理员已审核通过,大约5~10分钟部署完成!'
        elif status == 'F':
            msg = obj.image_name + ':' + obj.image_tag + ' 部署失败!'
        elif status == 'D':
            msg = obj.image_name + ':' + obj.image_tag + ' 已通知管理员审核!'
        Ding().msg(msg).at(current_user.mobile).send()
    else:
        obj.pro = status
    obj.save()
