# from app import db
# import datetime

# class Build(db.Model):
#     __tablename__ = 'builds'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(48), nullable=False)
#     tag = db.Column(db.String(48), nullable=False)
#     branch = db.Column(db.String(50), nullable=False)
#     status = db.Column(db.String(30), nullable=False)
#     command = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.datetime.now)
#
#     def __repr__(self):
#         return '<build {} {}>'.format(self.name, self.tag)
#
from mongoengine import *
from datetime import datetime


class Build(Document):
    name = StringField(required=True)
    tag = StringField(required=True)
    branch = StringField(required=True)
    status = StringField
    command = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
