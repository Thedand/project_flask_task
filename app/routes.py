from datetime import datetime

from flask import render_template, redirect, url_for, flash, request, abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, TaskForm
from app.models import User, Task


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        return render_template('home.html')


@app.route('/index', methods=['GET'])
@login_required
def index():
    q = request.args.get('q')

    if q:
        tasks = Task.query.filter(Task.title.contains(q) | Task.description.contains(q)).all()
    else:
        tasks = Task.query.order_by(Task.created_by.desc())
    return render_template('index.html', tasks=tasks)


# Add view with a list of usernames and amount of their tasks
@app.route('/crt', methods=['GET', 'POST'])
@login_required
def can_review_tasks():
    if current_user.can_review_tasks:
        pass
    else:
        return abort(403)
    users = db.session.query(User).all()
    return render_template('crt.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", "success")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_superuser:
            return current_user.is_authenticated
        else:
            abort(403)
        return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    is_active=True, is_superuser=False,
                    can_review_tasks=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations! You are now a registered user.", "success")
        return redirect(url_for('login'))
    return render_template('auth/registration.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


# Block /admin is not superuser
@app.route('/admin')
@login_required
def admin():
    if current_user.is_superuser:
        pass
    else:
        abort(403)
    return redirect(url_for('home'))


# Create Task
@app.route('/task/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.is_superuser:
        pass
    else:
        return abort(403)
    user_list = [(i.id, i.username) for i in User.query.all()]  # List users for create task
    form = TaskForm()
    form.user_id.choices = user_list
    if form.validate_on_submit():
        task = Task(title=form.title.data,
                    description=form.description.data,
                    lower_limit=form.lower_limit.data,
                    upper_limit=form.upper_limit.data,
                    created_at=form.created_at.data,
                    user_id=form.user_id.data)
        db.session.add(task)
        db.session.commit()
        flash("Your task has been created!", "success")
        return redirect(url_for('index'))
    return render_template('create.html', title='New Task',
                           form=form, legend='New Task')


# Update Task
@app.route('/task/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    if current_user.is_superuser:
        pass
    else:
        return abort(403)
    user_list = [(i.id, i.username) for i in User.query.all()]  # List users for update task
    task = Task.query.filter(Task.id == id).first()
    if request.method == 'POST':
        form = TaskForm(formdata=request.form, obj=id)
        form.populate_obj(task)
        db.session.commit()
        flash("Your task has been updated!", "success")
        return redirect(url_for('index', id=task.id))
    form = TaskForm(obj=task)
    form.user_id.choices = user_list
    return render_template('update.html', title='Update Task',
                           form=form, task=task, legend='Update Task')


# Task Deletion
@app.route('/task/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    if current_user.is_superuser:
        pass
    else:
        return abort(403)
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Your task has been deleted!", "success")
    return redirect(url_for('index'))
