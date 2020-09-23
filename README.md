# Task Manager

### Introduction

This is a task manager application, implemented using Flask with both the database (PostgreSQL). It also has user registration and authentication functionalities.
It is also available to create, update and delete tasks using the only superuser access flag. You can view the list of users and the number of their tasks with 
superuser access and users with access flag.

### Demo

![app](https://user-images.githubusercontent.com/17044897/93980229-08e72600-fd87-11ea-92d0-977d5ca532bd.gif)


### Files in the program
- main.py: Run app.
- config.py: Contains settings.
- routes.py: This is contains both the registration/login page logic, create/update/delete task and review task.
- models.py: Contains Flask-SQLAlchemy models used for user registration/login and task in routes.py
- forms.py: Contains the classes for WTForms/Flask-WTF and the custom validators for the fields.
- error.py: Contains errorhandler.
- requirements.txt: list of Python packages installed.
- templates/: folder with all HTML files
- static/: for with all CSS files, JS scripts and Demo gif.


## Usage

## Modify app

Modify config.py to replace the secret key (i.e. os.environ.get('SECRET')) with a secret key of your choice
and the database link (i.e. os.environ.get('DATABASE_URL')) with the link to your own database.

The two lines to be edited in config.py are shown below:

```
app.secret_key=os.environ.get('SECRET')
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
```

## Installations from the terminal
```shell script
mkdir Projects
cd Projects
git clone https://github.com/Thedand/project_flask_task.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

#### Import in python console
```python
> from app import app, db
> from app.models import User
> from app.routes import User
```
#### Add superuser
```python
> admin = User(username='admin', is_active=True, is_superuser=True, can_review_tasks=True)
> admin.set_password('admin')
> db.session.add(admin)
> db.session.commit()
```

Then simply open up a browser, Chrome/Chromium recommended, to [127.0.0.1:5000](https://127.0.0.1:5000/) / [localhost:5000](https://localhost:5000/)
