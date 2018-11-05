from orator import Model
from flask import abort
from models import Base
from orator.orm import scope
import re


class Image(Model, Base):

    @staticmethod
    def create_new(form):
        result = Image.insert({
            'name': form.get('name'),
            'tag': form.get('tag'),
            'host': form.get('host'),
            'port': form.get('port'),
            'notify': form.get('notify'),
            'command': re.sub(r'(-[vpe])', r'\\\n\1', form.get('command')),
            'image_name': form.get('image_name'),
            'git_branch': form.get('branch'),
            'git_message': form.get('message'),
            'code_registry': form.get('code_registry'),
            'dockerfile': form.get('dockerfile')
        })
        return result

    @scope
    def find_by_name(self, query, name):
        return query.where('name', name)

    @scope
    def find_by_tag(self, query, tag):
        return query.where('tag', tag).first()

    @scope
    def find_by_tags(self, query, tags: list):
        return query.where_in('tag', tags)

    # @scope
    # def find_one(self, query, args: dict):
    #     for k, v in args:
    #         query.where(k, v)
    #     return query.first()

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
