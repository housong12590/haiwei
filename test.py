from app import db
import datetime


class Build(db.Model):
    __tablename__ = 'builds'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), nullable=False)
    tag = db.Column(db.String(48), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    command = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<build {} {}>'.format(self.name, self.tag)
