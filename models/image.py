from orator import Model
from flask import abort
from orator.orm import scope
import re


class Image(Model):

    @staticmethod
    def create_new(form):
        image = Image()
        image.name = form.get('name')
        image.tag = form.get('tag')
        image.host = form.get('host')
        image.port = form.get('port')
        image.notify = form.get('notify')
        image.command = re.sub(r'(-[vpe])', r'\\\n\1', form.get('command'))
        image.image_name = form.get('image_name')
        image.git_branch = form.get('branch')
        image.git_message = form.get('message')
        image.code_registry = form.get('code_registry')
        # image.dockerfile = form.get('dockerfile')
        image.save()
        return image

    @scope
    def find_by_name(self, query, name):
        return query.where('name', name)

    @scope
    def find_by_tag(self, query, tag):
        return query.where('tag', tag).first()

    @scope
    def find_by_tags(self, query, tags: list):
        return query.where_in('tag', tags)

    @scope
    def find_one(self, query, args: dict):
        for k, v in args:
            query.where(k, v)
        return query.first()

    @scope
    def find_or_404(self, query, args: dict):
        for k, v in args:
            query.where(k, v)
        image = query.first()
        if image is None:
            abort(404)
        else:
            return image

    @scope
    def find_last_image(self, query, name):
        return query.where('name', name).order_by('tag', 'desc').first()

    def __repr__(self):
        return self.to_json()
