from orator import Model


class Deploy(Model):

    def __repr__(self):
        return self.to_json()

