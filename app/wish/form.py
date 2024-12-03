from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL
from ..util.field_length import FieldLength, length_max

IMAGE_ONLY = 'Images only'

class WishForm(FlaskForm):
  id = HiddenField('ID')
  description = StringField('Description', validators=[
    DataRequired(),
    Length(max=FieldLength.MEDIUM.value, message=length_max(FieldLength.MEDIUM.value))])
  url = StringField('Link', validators=[
    Optional(),
    URL(message="Enter valid URL"),
    Length(max=FieldLength.LARGE.value, message=length_max(FieldLength.LARGE.value))])
  image = FileField('Image', validators=[
    Optional(),
    FileAllowed(['gif', 'jpg', 'jpeg', 'png'], message=IMAGE_ONLY)])
  submit = SubmitField('Save Wish')
