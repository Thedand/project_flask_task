from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
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

from app.models import Task, User, Role

admin = Admin(app, name='Task Manager', template_mode='bootstrap3')
admin.add_view(ModelView(Task, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))

from app import routes
