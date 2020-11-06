from datetime import datetime

from app import db


class Task(db.Model):
    """ Task model """

    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    lower_limit = db.Column(db.Float)
    upper_limit = db.Column(db.Float)
    created_at = db.Column(db.Float)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Task {}>".format(self.title)