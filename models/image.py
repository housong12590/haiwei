from orator import Model
from flask import abort
from orator.orm import scope
import re


class Image(Model):

    def __repr__(self):
        return self.to_json()
