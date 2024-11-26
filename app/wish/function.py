import os
from flask import current_app as app, flash
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from .model import Wish
from .. import db

def save_file(file):
  filename = secure_filename(file.filename)
  file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

  try:
    file.save(file_path)
    return filename
  except Exception as e:
    flash(f'Error saving file: {e}', 'error')
    return None

def fill_wish(form, wish=None):
  wish = wish or Wish(owner=current_user)
  form.populate_obj(wish)
  return wish

def save_wish(wish):
  try:
    if wish.id is None:
      db.session.add(wish)
    db.session.commit()
    flash('Wish saved', 'success')
    return True
  except SQLAlchemyError as e:
    db.session.rollback()
    flash(f'Wish not saved: {str(e)}', 'error')
    return False

def handle_wish(form, wish=None):
  if form.validate_on_submit():
    filename = save_file(form.image.data) if form.image.data else None
    wish = fill_wish(form, wish)
    wish.image = filename or wish.image

    return save_wish(wish)

  return False

def toggle_wish(wish):
  try:
    if wish.is_buyer:
      wish.buyer = None
      flash('wish cancelled', 'success')
    else:
      wish.buyer = current_user
      flash('Wish bought', 'success')
    db.session.commit()
    return True
  except SQLAlchemyError as e:
    db.session.rollback()
    flash('Wish not updated', 'danger')
    return False
