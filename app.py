

from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from forms import LoginForm, RegistrationForm


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Nikita'}
    tasks = [
        {
            'author': {'username': 'Nikita'},
            'body': 'Create login and registration on site!'
        }
    ]
    return render_template('index.html', title='Home', user=user, tasks=tasks)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('/index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('/login'))
    return render_template('register.html', title='Sing Up', form=form)


if __name__ == '__main__':
    app.run(debug=True)
