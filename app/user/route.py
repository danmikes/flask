from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from .form import LoginForm, RegistrationForm
from .model import User
from ..util.flash import flash_errors
from .. import db

user = Blueprint('user', __name__, static_folder='', template_folder='')

@user.route('/user/login', methods=['GET', 'POST'])
def user_login():
  if current_user.is_authenticated:
    return redirect(url_for('wish.wishes'))

  form = LoginForm()
  if form.validate_on_submit():
    try:
      user = User.query.filter_by(username=form.username.data).first()
      if user and user.check_password(form.password.data):
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
          next_page = url_for('wish.wishes')
        return redirect(next_page)
      else:
        flash('Invalid credentials', 'danger')
    except Exception as e:
      current_app.logger.error(f'Error during login: {e}')
      flash('Error during login; retry', 'danger')

  flash_errors(form)
  return render_template('user/login.htm', form=form, page='login')

@user.route('/user/register', methods=['GET', 'POST'])
def user_register():
  if current_user.is_authenticated:
    return redirect(url_for('wish.wishes'))

  form = RegistrationForm()
  if form.validate_on_submit():
    if User.query.filter_by(username=form.username.data).first():
      flash('Username already exists; choose different username.', 'warning')
    else:
      new_user = User(username=form.username.data)
      new_user.set_password(form.password.data)
      try:
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can log in.', 'success')
        return redirect(url_for('user.user_login'))
      except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error during registration: {e}')
        flash('Error during registration; retry', 'danger')

  flash_errors(form)
  return render_template('user/register.htm', form=form, page='register')

@user.route('/user/logout')
@login_required
def user_logout():
  logout_user()
  flash('You have been logged out', 'success')
  return redirect(url_for('user.user_login'))

@user.route('/users/json', methods=['GET'])
# @login_required
def users_json():
  users = User.query.all()
  user_list = [user.to_dict() for user in users]
  return jsonify(user_list)
