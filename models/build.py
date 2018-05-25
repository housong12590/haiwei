from orator import Model
from orator.orm import scope
from app import db


class Build(Model):

    @scope
    def project_last_tag(self, query):
        result = db.select(
            "SELECT * FROM builds WHERE tag IN (SELECT max(tag) FROM builds GROUP BY name);")
        return result
