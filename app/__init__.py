from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
login.login_view = 'users.login'
login.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    with app.app_context():
        from app.models import User, Task

        db.create_all()

        from app.main.routes import main
        from app.users.routes import users
        from app.tasks.routes import tasks
        from app.errors.handlers import errors
        app.register_blueprint(main)
        app.register_blueprint(users)
        app.register_blueprint(tasks)
        app.register_blueprint(errors)

        from app.main.routes import Controller

        admin = Admin(app, name='Task Manager', template_mode='bootstrap3')
        admin.add_view(Controller(Task, db.session))
        admin.add_view(Controller(User, db.session))

        # Loading User
        @login.user_loader
        def load_user(user_id):
            if user_id is not None:
                return db.session.query(User).get(int(user_id))
            return None

        from app import errors

        return app
