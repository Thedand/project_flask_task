from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField
from wtforms.validators import InputRequired


class TaskForm(FlaskForm):
    """ Task Form """
    title = StringField('Task', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    lower_limit = FloatField('Lower limit', validators=[InputRequired()])
    upper_limit = FloatField('Upper limit', validators=[InputRequired()])
    created_at = FloatField('Created at', validators=[InputRequired()])
    user_id = SelectField('User', coerce=str, validators=[InputRequired()])