from flask import Blueprint

build = Blueprint('build', __name__)

from . import api
from . import views
