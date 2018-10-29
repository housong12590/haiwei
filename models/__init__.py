from orator.orm import scope
from .environ import Environ
from .image import Image
from .project import Project


class Base(object):

    @scope
    def find_one(self, query, args: dict):
        for k, v in args.items():
            query.where(k, v)
        return query.first()

    @scope
    def find_all(self, query, args: dict):
        for k, v in args.items():
            query.where(k, v)
        return query.get()

    @scope
    def find_or_404(self, query, args: dict):
        for k, v in args.items():
            query.where(k, v)
        return query.first()
