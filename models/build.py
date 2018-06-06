from orator import Model
from orator.orm import scope, accessor
from app.helper import utc2local, get_environs
import re


class Build(Model):
    __casts__ = {'status': 'bool', 'send': 'bool'}

    @staticmethod
    def create_new(form):
        build = Build()
        build.name = form.get('name')
        build.tag = form.get('tag')
        build.branch = form.get('branch')
        build.host = form.get('host')
        build.port = form.get('port')
        build.notify = form.get('notify')
        build.command = re.sub(r'(-[vpe])', r'\\\n\1', form.get('command'))
        build.image_name = form.get('image_name')
        build.send = bool(form.get('send'))
        build.dockerfile = form.get('dockerfile')
        build.code_registry = form.get('code_registry')
        build.message = form.get('message')
        build.save()
        return build

    @scope
    def find_by_name(self, query, name):
        return query.where('name', name)

    @scope
    def find_by_tag(self, query, tag):
        if tag is None:
            return None
        return query.where('tag', tag).first()

    @scope
    def find_by_tags(self, query, tags: list):
        if isinstance(tags, list):
            return query.where_in('tag', tags)
        else:
            raise TypeError('tags not iterable')

    @scope
    def last_image(self, query, name):
        return query.where('name', name).order_by('tag', 'desc')

    @scope
    def last_deploy_image(self, query, name):
        return query.where('name', name).where('status', 2).order_by('tag', 'desc').frist()

    @staticmethod
    def environs_change(tag, env_dict):
        build = Build.find_by_tag(tag).first()
        if build is None:
            return []
        last_cmd = get_environs(build.command)
        diff_set = set(last_cmd.items()) ^ set(env_dict.items())
        diff_set = set(item[0] for item in diff_set)
        return list(diff_set)

    @accessor
    def created_at(self):
        created_at = self.get_raw_attribute('created_at')
        return utc2local(created_at)

    def __repr__(self):
        return self.to_json()
