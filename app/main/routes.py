from flask import Blueprint, redirect, url_for, render_template, request, abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required

from app import db
from app.models import User, Task

main = Blueprint('main', __name__)


class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated \
                and current_user.is_superuser:
            pass
        else:
            abort(403)
        return redirect(url_for('main.index'))


# Home Page URL Route
@main.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    else:
        return render_template('main/home.html')


# Home Page URL Route
@main.route('/index', methods=['GET'])
@login_required
def index():
    q = request.args.get('q')
    # Sorted by tasks, description by creation date
    if q:
        tasks = db.session.query(Task).filter(Task.title.contains(q) | Task.description.contains(q)).all()
    else:
        tasks = db.session.query(Task).order_by(Task.created_by.desc())
    return render_template('main/index.html', tasks=tasks)


# Add view with a list of usernames and amount of their tasks
@main.route('/crt', methods=['GET', 'POST'])
@login_required
def can_review_tasks():
    # Checking the user is there access to the flag can_review_tasks
    if current_user.can_review_tasks:
        pass
    else:
        return abort(403)
    users = db.session.query(User).all()
    return render_template('main/crt.html', users=users)
