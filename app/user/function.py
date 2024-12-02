from flask import flash, redirect, url_for
from flask_login import login_user
from werkzeug.urls import url_parse
from ..util.flash import flash_errors
from ..util.logger import log
from .. import db
from .model import User

def handle_login(form, request):
  if form.validate_on_submit():
    try:
      user = User.query.filter_by(username=form.username.data).first()
      if user and user.check_password(form.password.data):
        login_user(user)
        flash('You logged-in', 'success')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
          next_page = url_for('wish.wishes')
        return redirect(next_page)
      else:
        flash('Invalid credentials', 'danger')
    except Exception as e:
      log.error(f'Error during login: {e}')
      flash('Error during login; retry', 'danger')

  flash_errors(form)
  return None

def handle_register(form):
  if form.validate_on_submit():
    if User.query.filter_by(username=form.username.data).first():
      flash('Username exists; choose another.', 'warning')
    else:
      new_user = User(username=form.username.data, password=form.password.data)
      try:
        db.session.add(new_user)
        db.session.commit()
        flash('You registered', 'success')
        return redirect(url_for('user.user_login'))
      except Exception as e:
        db.session.rollback()
        log.error(f'Registration failed: {e}')
        flash('Registration failed', 'danger')

  flash_errors(form)
  return None
