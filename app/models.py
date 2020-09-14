from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    can_review_tasks = db.relationship('Task', backref="author", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)

    def __init__(self, username, is_active, is_superuser):
        self.username = username
        self.is_active = is_active
        self.is_superuser = is_superuser

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Loading A User
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    lower_limit = db.Column(db.Float)
    upper_limit = db.Column(db.Float)
    created_at = db.Column(db.Float)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "<Task {}>".format(self.title)
