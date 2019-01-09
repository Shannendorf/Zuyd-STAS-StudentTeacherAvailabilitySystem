"""
    app.admin.forms
    ===============
    Forms used within the admin panel
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Location

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LocationForm(FlaskForm):
    """Form for adding a new location"""
    name = StringField('Name', validators=[DataRequired()])
    building = StringField('Building', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_locationname(self, name):
        location = Location.query.filter_by(Name=name.data).first()
        if location is not None:
            raise ValidationError('Please use a different location name.')