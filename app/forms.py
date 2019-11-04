from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,SelectField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee


class TaskForm(FlaskForm):
    """
    Form for manager to add or edit a TASK
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    status = SelectField('Status',choices = [('C', 'Created'),
      ('P', 'In progress'),('D','Deleted')])
    importance = SelectField('How Important it is?', choices=[('H', 'HIGH'),
                                            ('M', 'Medium'), ('L', 'Low')])
    towhom = StringField('To Whom it is assigned?',validators=[DataRequired()])

    submit = SubmitField('Submit')