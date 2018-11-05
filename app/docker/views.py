from . import docker as app
from orator.exceptions.query import QueryException
from flask import request, render_template, redirect, url_for
from app.helper import make_response
from models import Project, Image, OriginProject
import re


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


@app.route('/')
def index():
    projects = Project.order_by('deploy_id', 'asc').get()
    for project in projects:
        last_image = Image.where('image_name', project.image_name) \
            .order_by('image_tag', 'desc').first()
        project.image = last_image
    image_names = Image.group_by('image_name').lists('image_name')
    return render_template('docker/index.html', projects=projects, image_names=image_names)


@app.route('/project/<project_id>', methods=['GET', 'POST'])
@app.route('/project/create', methods=['GET', 'POST'])
def create_project(project_id=None):
    if request.method == 'GET':
        projects = OriginProject.all()
        image_names = Image.group_by('image_name').lists('image_name')
        project = None
        if project_id:
            project = Project.find(project_id)
        return render_template('docker/project/create.html',
                               project=project,
                               image_names=image_names,
                               projects=projects)
    image_name = request.form.get('image_name')
    origin_project_id = request.form.get('project_id')
    auto_deploy = bool(request.form.get('auto_deploy'))
    origin_project = OriginProject.find(origin_project_id)
    if project_id is None:
        Project.insert({
            'name': origin_project.name,
            'deploy_id': origin_project.id,
            'image_name': image_name
        })
    else:
        project = Project.find(project_id)
        project.name = project.name
        project.deploy_id = origin_project.id
        project.image_name = image_name
        project.save()
    return redirect(url_for('docker.index'))


@app.route('/update')
def update():
    pass


@app.route('/images')
def images():
    data = Image.order_by('image_tag', 'desc').get()
    return render_template('docker/images.html', images=data)
