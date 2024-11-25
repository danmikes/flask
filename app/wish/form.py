from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional, URL

class WishForm(FlaskForm):
  id = HiddenField('ID')
  description = StringField('Description', validators=[
    DataRequired()])
  url = StringField('Link', validators=[
    Optional(),
    URL(message="Enter valid URL")])
  image = FileField('Image', validators=[
    Optional(),
    FileAllowed(['gif', 'jpg', 'jpeg', 'png'], 'Images only')])
  submit = SubmitField('Save Wish')
