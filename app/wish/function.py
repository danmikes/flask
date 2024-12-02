import os
from flask import current_app, flash
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from .model import Wish
from ..util.logger import log
from .. import db

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file):
  if not allowed_file(file.filename):
    flash('Invalid file type', 'error')
    return None

  upload_folder = current_app.config['UPLOAD_FOLDER']
  filename = secure_filename(file.filename)
  file_path = os.path.join(upload_folder, filename)

  os.makedirs(upload_folder, exist_ok=True)

  try:
    file.save(file_path)
    return filename
  except Exception as e:
    flash(f'Error saving file: {e}', 'error')
    return None

def delete_file(file):
  pass

def fill_wish(form, wish=None):
  wish = wish or Wish(owner=current_user, description='', url=None, image=None)

  wish.description = form.description.data
  wish.url = form.url.data if form.url.data else None
  wish.image = form.image.data if form.image.data else None

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

def delete_wish(wish):
  try:
    db.session.delete(wish)
    db.session.commit()
    flash('Wish deleted', 'success')
    return None
  except Exception as e:
    db.session.rollback()
    flash(f'Error deleting wish: {str(e)}', 'error')
    return wish

def handle_wish(form, wish=None):
  if form.validate_on_submit():
    filename = save_file(form.image.data)
    wish = fill_wish(form, wish)
    wish.image = filename or wish.image
    return save_wish(wish)
  return False

def toggle_wish(wish):
  try:
    if wish.is_buyer:
      wish.buyer = None
      flash('Wish cancelled', 'danger')
    else:
      wish.buyer = current_user
      flash('Wish bought', 'info')
    db.session.commit()
    return True
  except SQLAlchemyError as e:
    db.session.rollback()
    flash('Wish not updated', 'danger')
    return False
