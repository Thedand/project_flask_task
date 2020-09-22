from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Database Initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app.routes import Controller
from app.models import Task, User

admin = Admin(app, name='Task Manager', template_mode='bootstrap3')
admin.add_view(Controller(Task, db.session))
admin.add_view(Controller(User, db.session))

# Create DB
db.create_all()
db.session.commit()

from app import errors
