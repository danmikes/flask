from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from ..form.login import LoginForm, RegistrationForm
from ..model.user import User
from ..util.util import flash_errors
from .. import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.wish'))

  form = LoginForm()
  if form.validate_on_submit():
    try:
      user = User.query.filter_by(username=form.username.data).first()
      if user and user.check_password(form.password.data):
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
          next_page = url_for('main.wish')
        return redirect(next_page)
      else:
        flash('Invalid credentials', 'danger')
    except Exception as e:
      current_app.logger.error(f'Error during login: {e}')
      flash('Error during login; retry', 'danger')

  flash_errors(form)
  return render_template('auth/login.htm', form=form, page='login')

@auth.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.wish'))

  form = RegistrationForm()
  if form.validate_on_submit():
    # ToDo : check email
    if User.query.filter_by(username=form.username.data).first():
      flash('Username already exists; choose different username.', 'warning')
    else:
      new_user = User(username=form.username.data)
      new_user.set_password(form.password.data)
      try:
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can log in.', 'success')
        return redirect(url_for('auth.login'))
      except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error during registration: {e}')
        flash('Error during registration; retry', 'danger')

  flash_errors(form)
  return render_template('auth/register.htm', form=form)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have been logged out', 'success')
  return redirect(url_for('auth.login'))

@auth.route('/users/json', methods=['GET'])
@login_required
def users_json():
  users = User.query.all()
  user_list = [user.to_dict() for user in users]
  return jsonify(user_list)
