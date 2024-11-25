import os
from flask import current_app, flash
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from .model import Wish
from .. import db

def save_file(file):
  if file:
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    try:
      file.save(file_path)
    except Exception as e:
      flash(f'Error saving file: {e}', 'error')
      return False
  return False

def fill_wish(form, wish=None):
  if wish is None:
    wish = Wish(owner=current_user)

  form.populate_obj(wish)
  return wish

def save_wish(wish):
  try:
    if wish.id is None:
      db.session.add(wish)
    db.session.commit()
    flash('Wish saved', 'success')
    return True, None
  except SQLAlchemyError as e:
    db.session.rollback()
    flash(f'Wish not saved: {str(e)}', 'error')
    return False, wish

def handle_wish(form, wish=None):
  if form.validate_on_submit():
    file = form.image.data if 'image' in form else None
    filename = save_file(file)

    wish = fill_wish(form, wish)
    wish.image = filename if filename else wish.image

    save_wish(wish)

  return False, None
