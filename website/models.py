from . import db
from flask_login import UserMixin # type: ignore

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gk = db.Column(db.String(100))
    cb = db.Column(db.String(100))
    cm = db.Column(db.String(100))
    wf = db.Column(db.String(100))
    st = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def serialize(self):
        return {
            'id': self.id,
            'gk': self.gk,
            'cb': self.cb,
            'cm': self.cm,
            'wf': self.wf,
            'st': self.st,
            'user_id': self.user_id
        }

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    teams = db.relationship('Team', backref='user', lazy=True)
