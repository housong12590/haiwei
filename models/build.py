from orator import Model
from orator.orm import scope


class Build(Model):

    @scope
    def project_last_images(self, query):
        builds = query.select(query.raw('max(tag) as tag')).group_by('name').get()
        tags = [build.tag for build in builds]
        return Build.where_in('tag', tags)

    @scope
    def project_detail(self, query, name, tag):
        return query.where('name', name).where('tag', tag)

    def __repr__(self):
        return self.to_json()