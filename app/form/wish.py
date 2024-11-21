from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Optional, URL

class WishForm(FlaskForm):
  description = StringField('Description', validators=[DataRequired()])
  # ToDo : url -> urlList
  url = StringField('Link', validators=[Optional(), URL(message="Enter valid URL")])
  img = FileField('Image', validators=[
    Optional(),
    FileAllowed(['gif', 'jpg', 'jpeg', 'png'], 'Images only')
  ])
  submit = SubmitField('Add Wish')
