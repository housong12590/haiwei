from orator import Model

from flask_login.mixins import UserMixin


class User(UserMixin, Model):

    def __repr__(self):
        return self.to_json()
