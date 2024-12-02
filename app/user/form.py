from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

LENGTH_MAX = 20
def length_max(max=LENGTH_MAX):
  return f'Maximum length is {max} characters'

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[
    DataRequired(),
    Length(min=3, max=20, message=length_max(LENGTH_MAX))])
  password = PasswordField('Password', validators=[
    DataRequired(),
    Length(min=3, max=20, message=length_max(LENGTH_MAX))])
  submit = SubmitField('Log-In')

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[
    DataRequired(),
    Length(min=3, max=20, message=length_max(LENGTH_MAX))])
  password = PasswordField('Password', validators=[
    DataRequired(),
    Length(min=3, max=20, message=length_max(LENGTH_MAX))])
  confirm_password = PasswordField('Confirm Password', validators=[
    DataRequired(),
    EqualTo('password'),
    Length(min=3, max=20, message=length_max(LENGTH_MAX))])
  submit = SubmitField('Register')
