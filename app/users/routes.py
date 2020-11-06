from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse

from app import db
from app.users.forms import LoginForm, RegistrationForm
from app.users.models import User

users = Blueprint('users', __name__)


# User Login Form URL Route
@users.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user = db.session.query(User) \
            .filter_by(username=login_form.username.data).first()
        if user is None or not user \
                .check_password(login_form.password.data):
            flash("Invalid username or password.", "danger")
            return redirect(url_for('users.login'))
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=login_form)


# User Logout
@users.route('/logout', methods=['GET'])
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('main.home'))


# User Registration
@users.route('/registration', methods=['GET', 'POST'])
def registration():
    reg_form = RegistrationForm()

    # Update database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        password_hash = generate_password_hash(password)

        # Add username & hashed password to DB
        # Created default settings users with flags(active, superuser, can_review_tasks)
        user = User(username=username,
                    password_hash=password_hash,
                    is_active=True,
                    is_superuser=True,
                    can_review_tasks=True)
        db.session.add(user)
        db.session.commit()

        flash("Congratulations! You are now a registered user.", "success")
        return redirect(url_for('users.login'))

    return render_template('auth/registration.html', form=reg_form)


# User account
@users.route('/account')
@login_required
def account():
    return render_template('auth/account.html', title='Account')


# Block /admin is not superuser
@users.route('/admin')
@login_required
def admin():
    # Checking the user to superuser
    if current_user.is_superuser:
        pass
    else:
        abort(403)
    return redirect(url_for('main.home'))
