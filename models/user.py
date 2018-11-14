from orator import Model


class User(Model):

    def __repr__(self):
        return self.to_json()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
