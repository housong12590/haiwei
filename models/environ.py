from orator import Model
from orator.orm import scope


class Environ(Model):

    def __repr__(self):
        return self.to_json()
