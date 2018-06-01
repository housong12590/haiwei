from orator import Model
from orator.orm import scope, accessor
from app.helper import utc2local


class Build(Model):
    __casts__ = {'status': 'bool', 'send': 'bool'}

    @scope
    def project_last_images(self, query):
        builds = query.select(query.raw('max(tag) as tag')).group_by('name').get()
        tags = [build.tag for build in builds]
        return Build.where_in('tag', tags)

    @scope
    def project_detail(self, query, name, tag):
        return query.where('name', name).where('tag', tag)

    @accessor
    def created_at(self):
        created_at = self.get_raw_attribute('created_at')
        return utc2local(created_at)

    def __repr__(self):
        return self.to_json()
