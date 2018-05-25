from . import build as app
from flask import request, render_template
from models import Build
from orator.exceptions.query import QueryException
from app.helper import make_response
import re


@app.route('/record', methods=['POST'])
def record():
    try:
        Build.insert(
            name=request.form.get('name'),
            tag=request.form.get('tag'),
            status=request.form.get('status'),
            branch=request.form.get('branch'),
            host=request.form.get('host'),
            port=request.form.get('port'),
            notify=request.form.get('notify'),
            command=re.sub(r'(-[vpe])', r'\\\n\1', request.form.get('command')),
            image_name=request.form.get('image_name'),
            end=request.form.get('send'),
            dockerfile=request.form.get('dockerfile')
        )
    except QueryException as e:
        return make_response('fail', 404, e.args)
    return make_response('success')


@app.route('/index')
def index():
    data = Build.project_last_tag()
    return render_template('build/index.html', data=data)


@app.route('/<project>/<tag>')
def detail(project, tag):
    build = Build.where('name', project).where('tag', tag).first_or_fail()
    build.command = build.command.replace('\n', '<br/>')
    return render_template('build/detail.html', data=build)


@app.route('/<project>')
def images(project):
    data = Build.where('name', project).order_by('tag', 'desc').get()
    return render_template('build/images.html', data=data)
