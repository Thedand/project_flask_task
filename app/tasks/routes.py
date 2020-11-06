from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required

from app import db
from app.forms import TaskForm
from app.models import User, Task

tasks = Blueprint('tasks', __name__)


# Create Task
@tasks.route('/task/create', methods=['GET', 'POST'])
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
            return redirect(url_for('main.index'))
        except IndexError:
            flash("There was an issue created your task!", "danger")
    return render_template('tasks/create.html', title='New Task',
                           form=form_task, legend='New Task')


# Update Task
@tasks.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index', task_id=task.id))

    form_task = TaskForm(obj=task)
    form_task.user_id.choices = user_list
    return render_template('tasks/update.html', title='Update Task',
                           form=form_task, task=task, legend='Update Task')


# Task Deletion
@tasks.route('/task/<int:task_id>/delete', methods=['POST'])
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
        return redirect(url_for('main.index'))
    except IndexError:
        flash("There was an problem deleting that task!", "danger")
