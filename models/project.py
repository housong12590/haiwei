from orator import Model
from orator.orm import scope


class Project(Model):

    @scope
    def find_name_or_new(self, query, name):
        pro = query.where('name', name).first()
        if pro is None:
            pro = Project()
            pro.name = name
            pro.save()
        return pro

    def __repr__(self):
        return self.to_json()
