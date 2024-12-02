from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL

LENGTH_MAX = 255
def length_max(max=LENGTH_MAX):
  return f'Maximum length is {max} characters'

image_only = 'Only images are allowed'

class WishForm(FlaskForm):
  id = HiddenField('ID')
  description = StringField('Description', validators=[
    DataRequired(),
    Length(max=LENGTH_MAX, message=length_max(LENGTH_MAX))])
  url = StringField('Link', validators=[
    Optional(),
    URL(message="Enter valid URL"),
    Length(max=LENGTH_MAX, message=length_max(LENGTH_MAX))])
  image = FileField('Image', validators=[
    Optional(),
    FileAllowed(['gif', 'jpg', 'jpeg', 'png'])])
  submit = SubmitField('Save Wish')
