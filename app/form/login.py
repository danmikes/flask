from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=3)])
  submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
  email = EmailField('Email', validators=[DataRequired(), Length(max=30)])
  username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=3)])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')
