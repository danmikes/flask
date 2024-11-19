from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from .form import LoginForm, RegistrationForm
from .model import User
from .util import flash_errors
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('view/index.htm')

@main.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.dashboard'))

  form = LoginForm()
  if form.validate_on_submit():
    try:
      user = User.query.filter_by(username=form.username.data).first()
      if user and user.check_password(form.password.data):
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
          next_page = url_for('main.dashboard')
        return redirect(next_page)
      else:
        flash('Invalid credentials', 'danger')
    except Exception as e:
      current_app.logger.error(f'Error during login: {e}')
      flash('Error during login; retry', 'danger')

  flash_errors(form)
  return render_template('view/login.htm', form=form, page='login')

@main.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.dashboard'))

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
        return redirect(url_for('main.login'))
      except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error during registration: {e}')
        flash('Error during registration; retry', 'danger')

  flash_errors(form)
  return render_template('view/register.htm', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
  return render_template('view/dashboard.htm', username=current_user.username)

@main.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have been logged out', 'success')
  return redirect(url_for('main.login'))
