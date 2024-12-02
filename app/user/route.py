from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from .form import LoginForm, RegistrationForm
from .model import User
from .function import handle_login, handle_register

user = Blueprint('user', __name__, url_prefix='/user', static_folder='.', template_folder='.')

@user.route('/login', methods=['GET', 'POST'])
def user_login():
  if current_user.is_authenticated:
    return redirect(url_for('wish.wishes'))

  form = LoginForm()
  result = handle_login(form, request)
  if result:
    return result
  return render_template('user/login.htm', form=form, page='login')

@user.route('/register', methods=['GET', 'POST'])
def user_register():

  form = RegistrationForm()
  result = handle_register(form)
  if result:
    return result
  return render_template('user/register.htm', form=form, page='register')

@user.route('/logout', methods=['GET'])
@login_required
def user_logout():
  logout_user()
  flash('You logged-out', 'success')
  return redirect(url_for('user.user_login'))

# ADMIN ONLY

@user.route('/all/json', methods=['GET'])
@login_required
def users_json():
  users = User.query.all()
  user_list = [user.to_dict() for user in users]
  return jsonify(user_list)

# ToDo : Complete
@login_required # Admin-only
@user.route('/add', methods=['GET', 'POST'])
def user_add():
  return 'user_add'

# ToDo : Complete
@login_required # Admin-only
@user.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def user_edit(user_id):
  return 'user_edit'

# ToDo : Complete
@login_required # Admin-only
@user.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def user_delete(user_id):
  return 'user_delete'

# ToDo : Complete
@login_required # Admin-only
@user.route('/all/delete', methods=['GET', 'POST'])
def users_delete():
  return 'users_delete'
