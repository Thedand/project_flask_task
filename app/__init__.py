from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

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

# Create an account Admin(superuser) and Guest(user)
db.create_all()
db.session.commit()
try:
    admin = User(username='admin', is_active=True, is_superuser=True)
    admin.set_password('admin')
    guest = User(username='guest', is_active=True, is_superuser=False)
    guest.set_password('guest')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
except IntegrityError:
    db.session.rollback()

from app import routes, models, errors
