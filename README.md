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
- database.cong: setting db
- Dockerfile: for build app
- docker-compose.yml: for build app, db and their connections


## Usage

## Modify app

Modify database.conf

```
POSTGRES_USER=postgres #default username
POSTGRES_PASSWORD=1591 #default password
POSTGRES_HOST=localhost #default or your url
POSTGRES_PORT=5432 #default or your port
POSTGRES_DB=db #default or your database
```

Modify docker-compose.yml

```
environment:
- POSTGRES_USER=postgres #database.conf
- POSTGRES_PASSWORD=1591 #database.conf
- POSTGRES_HOST=db #database.conf
- POSTGRES_PORT=5432 #database.conf
- POSTGRES_DB=db #database.conf

OR use instead environment

env_file: database.conf
```

## Installations from the terminal
```shell script
mkdir Projects
cd Projects
git clone https://github.com/Thedand/project_flask_task.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Installation docker and docker-compose

[Install Docker](https://docs.docker.com/get-docker/)

[Install Docker Compose](https://docs.docker.com/compose/install/)

#### Install using terminal


`cd project_flask_task`

`docker-compose up --build` frontend usage or build project

While the app and database are being created

Here are the commands to access the application and database

`docker exec -it project_flask_task_db_1 psql -U postgres` - access in Postgresql

`docker exec -it project_flask_task_app_1 bash` - access in app use bash

#### The default user is created with access flags
```
is_active=True - active, can log in task manager.
is_superuser=True - superuser, can create, edit and delete tasks.
can_review_tasks=True - can_review_tasks, can access to the number of tasks.
```
`you can change these access flags in routes.py -> User Registration`


#### Welcome to page Task Manager
`Then simply open up a browser, Chrome/Chromium recommended, to` [127.0.0.1:5000](https://127.0.0.1:5000/) / [localhost:5000](https://localhost:5000/)
