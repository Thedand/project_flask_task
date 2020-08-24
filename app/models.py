# from datetime import datetime

from flask_login import UserMixin
# from flask_security import RoleMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# self-join
# roles_users = db.Table('roles_users',
#                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#                        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
#                        )


# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    # roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    tasks = db.relationship('Task', backref="author", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


# Role
# class Role(db.Model, RoleMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     description = db.Column(db.String(128))


# Task Model
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    lower_limit = db.Column(db.Float)
    upper_limit = db.Column(db.Float)
    created_at = db.Column(db.Float)
    updated_at = db.Column(db.TIMESTAMP, onupdate=func.utc())
    created_by = db.Column(db.TIMESTAMP, default=func.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, title, description, lower_limit, upper_limit, created_at, created_by, user_id):
        self.title = title
        self.description = description
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.created_at = created_at
        self.created_by = created_by
        self.user_id = user_id

    def __repr__(self):
        return "<Task {}>".format(self.title)
