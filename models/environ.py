from orator import Model
from orator.orm import scope


class Environ(Model):

    @scope
    def find_default(self, query):
        return query.where('default', True)

    def __repr__(self):
        return self.to_json()
