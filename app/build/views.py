from . import build as app
from flask import request, render_template
from models import Build
from orator.exceptions.query import QueryException
from app.helper import make_response
import re


@app.route('/record', methods=['POST'])
def record():
    try:
        build = Build()
        build.name = request.form.get('name')
        build.tag = request.form.get('tag')
        build.status = request.form.get('status')
        build.branch = request.form.get('branch')
        build.command = re.sub(r'(-[vpe])', r'\\\n\1', request.form.get('command'))
        build.save()
    except QueryException as e:
        return make_response('fail', 404, e.args)
    return make_response('success')


@app.route('/index')
def index():
    # sql = "SELECT * FROM builds WHERE tag IN (SELECT max(tag) FROM builds GROUP BY name);"
    # data = db.session.execute(sql)
    build = Build()
    data = Build.project_last_tag()
    # for i in data:
    #     print(i)

    # print(Build.group_by('name').max('tag'))
    # data = build.where_in('tag', build.group_by('name').max('tag')).get()
    data = []
    return render_template('build/index.html', data=data)


@app.route('/<project>/<tag>')
def detail(project, tag):
    build = Build()
    build = build.where('name', project).where('tag', tag).first_or_fail()
    build.command = build.command.replace('\n', '<br/>')
    return render_template('build/detail.html', data=build)


@app.route('/<project>')
def images(project):
    build = Build()
    data = build.where('name', project).order_by('tab', 'desc').get()
    return render_template('build/images.html', data=data)
