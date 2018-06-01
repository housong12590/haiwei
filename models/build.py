from orator import Model
from orator.orm import scope, accessor
from app.helper import utc2local
import re


class Build(Model):
    __casts__ = {'status': 'bool', 'send': 'bool'}

    @staticmethod
    def create_new(form):
        build = Build()
        build.name = form.get('name')
        build.tag = form.get('tag')
        build.status = bool(form.get('status'))
        build.branch = form.get('branch')
        build.host = form.get('host')
        build.port = form.get('port')
        build.notify = form.get('notify')
        build.command = re.sub(r'(-[vpe])', r'\\\n\1', form.get('command'))
        build.image_name = form.get('image_name')
        build.send = bool(form.get('tag'))
        build.dockerfile = form.get('dockerfile')
        build.code_registry = form.get('code_registry')
        build.message = form.get('message')
        build.save()
        return build

    @scope
    def project_last_images(self, query):
        builds = query.select(query.raw('max(tag) as tag')).group_by('name').get()
        tags = [build.tag for build in builds]
        return Build.where_in('tag', tags)

    @scope
    def project_detail(self, query, name, tag):
        return query.where('name', name).where('tag', tag)

    @staticmethod
    def del_project(name):
        Build.where('name', name).delete()

    @scope
    def last_image(self, query, name):
        return query.where('name', name).order_by('tag', 'desc').first()

    @accessor
    def created_at(self):
        created_at = self.get_raw_attribute('created_at')
        return utc2local(created_at)

    def __repr__(self):
        return self.to_json()
