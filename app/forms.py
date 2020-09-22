from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
    BooleanField, SubmitField, TextAreaField, \
    FloatField, SelectField
from wtforms.validators import InputRequired, \
    EqualTo, ValidationError

from app import db
from app.models import User


class LoginForm(FlaskForm):
    """ Login form """

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Sing In')


class RegistrationForm(FlaskForm):
    """ Registration form"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(),
                                                 EqualTo('password',
                                                         message='Passwords must match')])
    submit = SubmitField('Sing Up')

    def validate_username(self, username):
        user_object = db.session.query(User).filter_by(username=username.data).first()
        if user_object:
            raise ValidationError('Username already exists. Select a different username.')


class TaskForm(FlaskForm):
    """ Task Form """
    title = StringField('Task', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    lower_limit = FloatField('Lower limit', validators=[InputRequired()])
    upper_limit = FloatField('Upper limit', validators=[InputRequired()])
    created_at = FloatField('Created at', validators=[InputRequired()])
    user_id = SelectField('User', coerce=str, validators=[InputRequired()])
