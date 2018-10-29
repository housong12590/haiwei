from . import docker as app
from flask import request
from app.helper import make_response
from models import Project, Image


@app.route('/push', methods=['POST'])
def push():
    project_name = request.form.get('project_name')
    image_args = {
        'project_name': project_name,
        'image_name': request.form.get('image_name'),
        'image_tag': request.form.get('image_tag'),
        'git_branch': request.form.get('git_branch'),
        'git_message': request.form.get('git_message'),
        'code_registry': request.form.get('code_registry'),
        'command': request.form.get('command'),
        'dockerfile': request.form.get('dockerfile')
    }
    Image.insert(image_args)
    project = Project.find_one({'name', project_name})
    if project is None:
        project_args = {
            'name': project_name,
            'image_name': request.form.get('image_name'),
            'last_image_id': request.form.get('image_')
        }
        Project.insert(project_args)
    return make_response()


def index():
    pass
