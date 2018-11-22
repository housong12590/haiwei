from orator import Model


class Project(Model):

    def __repr__(self):
        return self.to_json()
