from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField, FloatField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo, InputRequired

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sing In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sing Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class TaskForm(FlaskForm):
    title = StringField('Task', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    lower_limit = FloatField('Lower limit', validators=[DataRequired()])
    upper_limit = FloatField('Upper limit', validators=[DataRequired()])
    created_at = FloatField('Created at', validators=[DataRequired()])
    user_id = SelectField('User', coerce=str, validators=[InputRequired()])
