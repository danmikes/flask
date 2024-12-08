import os
from flask import current_app, flash
from flask_login import current_user
from PIL import Image
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from .model import Wish
from ..util.logger import log
from ..util.route import remove_unused_files
from .. import db

DIMENSION_MAX = 400

def get_upload_folder():
  return current_app.config['UPLOAD_FOLDER']

def allowed_file(file_name):
  return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def file_exists(file_name):
  file_path = os.path.join(get_upload_folder(), file_name)
  return os.path.exists(file_path)

def resize_image(image, dimension_max=DIMENSION_MAX):
  width, height = image.size

  if width > height:
    new_width = dimension_max
    new_height = int((height / width) * new_width)
  else:
    new_height = dimension_max
    new_width = int((width / height) * new_height)

  return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def save_file(file):
  file_name = secure_filename(file.filename)
  file_path = os.path.join(get_upload_folder(), file_name)

  os.makedirs(get_upload_folder(), exist_ok=True)

  try:
    with Image.open(file) as image:
      image_resized = resize_image(image)
      image_resized.save(file_path, dpi=(72, 72), quality=85)
      return file_name
  except Exception as e:
    flash(f'Error saving file: {e}', 'warning')
    return None

def delete_file(file_name):
  file_path = os.path.join(get_upload_folder(), file_name)
  try:
    os.remove(file_path)
    log.info(f'File removed: {file_name}')
    return None
  except Exception as e:
    log.info(f'File not removed: {file_name} : {e}')
  return file_name

def fill_wish(form, wish=None):
  wish = wish or Wish(owner=current_user, description='', url=None, image=None)

  wish.description = form.description.data
  wish.url = form.url.data if form.url.data else None
  wish.image = form.image.data if form.image.data else None

  return wish

def save_wish(wish=None):
  try:
    if wish.id is None:
      db.session.add(wish)
    db.session.commit()
    flash('Wish saved', 'info')
    remove_unused_files()
    return True
  except SQLAlchemyError as e:
    db.session.rollback()
    flash(f'Wish not saved: {str(e)}', 'info')
    return False

def delete_wish(wish):
  try:
    db.session.delete(wish)
    db.session.commit()
    flash('Wish deleted', 'info')
    remove_unused_files()

    return None
  except Exception as e:
    db.session.rollback()
    flash(f'Error deleting wish', 'warning')
    return wish

def process_wish(form, wish=None):
  if form.validate_on_submit():
    data = form.image.data
    filename = data.filename if data else None
    img_name = wish.image if wish else None

    if filename:
      if not allowed_file(filename):
        flash('Invalid file type', 'warning')
        return False

      if file_exists(filename):
        flash('File exists', 'warning')
        return False

      saved_file_name = save_file(data)
      if saved_file_name:
        img_name = saved_file_name
      else:
        flash('Error saving file', 'warning')

    if wish is None:
      wish = fill_wish(form)
    else:
      wish = fill_wish(form, wish)
    wish.image = img_name

    return save_wish(wish)
  return False

def add_wish(form):
  return process_wish(form)

def edit_wish(form, wish):
  return process_wish(form, wish)

def toggle_wish(wish):
  try:
    if wish.is_buyer:
      wish.buyer = None
      flash('Wish cancelled', 'warning')
    else:
      wish.buyer = current_user
      flash('Wish bought', 'info')
    db.session.commit()
    return True
  except SQLAlchemyError as e:
    db.session.rollback()
    flash('Wish not updated', 'warning')
    return False
