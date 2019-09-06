from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,SelectField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee,Task


class TaskForm(FlaskForm):
    """
    Form for admin to add or edit a TASK
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    status = SelectField('Status',choices = [('C', 'Created'),
      ('P', 'In progress'),('D','Deleted')])
    importance = SelectField('How Important it is?', choices=[('H', 'HIGH'),
                                            ('M', 'Medium'), ('L', 'Low')])
    towhom = StringField('To Whom it is assigned?',validators=[DataRequired()])

    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    """
    Form for users TO REGISTER
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
#not using first name and last name as this is done by admin
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Add Employee!!')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')