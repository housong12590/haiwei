from . import docker as app
from flask import request
from app.helper import make_response
from models import Project, Image
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
    Image.insert(image_args)
    return make_response()


def index():
    pass
