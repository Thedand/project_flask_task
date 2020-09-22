from flask import render_template, redirect, url_for, flash, request, abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, TaskForm
from app.models import User, Task


# Home Page URL Route
@app.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        return render_template('home.html')


# Home Page URL Route
@app.route('/index', methods=['GET'])
@login_required
def index():
    q = request.args.get('q')
    # Sorted by tasks, description by creation date
    if q:
        tasks = db.session.query(Task).filter(Task.title.contains(q) | Task.description.contains(q)).all()
    else:
        tasks = db.session.query(Task).order_by(Task.created_by.desc())
    return render_template('index.html', tasks=tasks)


# Add view with a list of usernames and amount of their tasks
@app.route('/crt', methods=['GET', 'POST'])
@login_required
def can_review_tasks():
    # Checking the user is there access to the flag can_review_tasks
    if current_user.can_review_tasks:
        pass
    else:
        return abort(403)
    users = db.session.query(User).all()
    return render_template('crt.html', users=users)


# User Login Form URL Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user = db.session.query(User) \
            .filter_by(username=login_form.username.data).first()
        if user is None or not user \
                .check_password(login_form.password.data):
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', form=login_form)


class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated \
                and current_user.is_superuser:
            pass
        else:
            abort(403)
        return redirect(url_for('index'))


# User Logout
@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))


# User Registration
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    reg_form = RegistrationForm()

    # Update database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        password_hash = generate_password_hash(password)

        # Add username & hashed password to DB
        user = User(username=username,
                    password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        flash("Congratulations! You are now a registered user.", "success")
        return redirect(url_for('login'))

    return render_template('auth/registration.html', form=reg_form)


# User account
@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


# Block /admin is not superuser
@app.route('/admin')
@login_required
def admin():
    # Checking the user to superuser
    if current_user.is_superuser:
        pass
    else:
        abort(403)
    return redirect(url_for('home'))


# Create Task
@app.route('/task/create', methods=['GET', 'POST'])
@login_required
def create():
    # Checking the user to superuser
    if current_user.is_superuser:
        pass
    else:
        return abort(403)

    # List users for create task
    user_list = [(i.id, i.username) for i in db.session.query(User).all()]
    form_task = TaskForm()
    form_task.user_id.choices = user_list
    if form_task.validate_on_submit():
        task = Task(title=form_task.title.data,
                    description=form_task.description.data,
                    lower_limit=form_task.lower_limit.data,
                    upper_limit=form_task.upper_limit.data,
                    created_at=form_task.created_at.data,
                    user_id=form_task.user_id.data)

        # Adding In DB
        try:
            db.session.add(task)
            db.session.commit()
            flash("Your task has been created!", "success")
            return redirect(url_for('index'))
        except IndexError:
            flash("There was an issue created your task!", "danger")
    return render_template('create.html', title='New Task',
                           form=form_task, legend='New Task')


# Update Task
@app.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update(task_id):
    if current_user.is_superuser:
        pass
    else:
        return abort(403)

    # Select list users for update task
    user_list = [(i.id, i.username) for i in db.session.query(User).all()]
    task = db.session.query(Task).filter(Task.id == task_id).first()

    if request.method == 'POST':
        form_task = TaskForm(formdata=request.form, obj=task_id)
        form_task.populate_obj(task)

        db.session.commit()
        flash("Your task has been updated!", "success")
        return redirect(url_for('index', task_id=task.id))

    form_task = TaskForm(obj=task)
    form_task.user_id.choices = user_list
    return render_template('update.html', title='Update Task',
                           form=form_task, task=task, legend='Update Task')


# Task Deletion
@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete(task_id):
    if current_user.is_superuser:
        pass
    else:
        return abort(403)
    task = db.session.query(Task).get_or_404(task_id)

    try:
        db.session.delete(task)
        db.session.commit()
        flash("Your task has been deleted!", "success")
        return redirect(url_for('index'))
    except IndexError:
        flash("There was an problem deleting that task!", "danger")
