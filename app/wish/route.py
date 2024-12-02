from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..user.model import User
from .form import WishForm
from .model import Wish
from .function import delete_wish, handle_wish, toggle_wish
from ..util.flash import flash_errors

wish = Blueprint('wish', __name__, url_prefix='/wish', static_folder='.', template_folder='.')

@wish.route('/all', methods=['GET'])
@login_required
def wishes():
  users_all = User.query.all()
  users_they = [user for user in users_all if user.id != current_user.id]

  return render_template('wish/view.htm', users_they=users_they)

@wish.route('/add', methods=['GET', 'POST'])
@login_required
def wish_add():
  form = WishForm()

  if request.method == 'POST':
    if handle_wish(form):
      return redirect(url_for('wish.wishes'))

  flash_errors(form)
  return render_template('wish/form.htm', form=form, is_edit=False)

@wish.route('/edit/<int:wish_id>', methods=['GET', 'POST'])
@login_required
def wish_edit(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  form = WishForm(obj=wish)

  if request.method == 'POST':
    if handle_wish(form, wish):
      return redirect(url_for('wish.wishes'))

  flash_errors(form)
  return render_template('wish/form.htm', form=form, is_edit=True)

@wish.route('/delete/<int:wish_id>', methods =['GET', 'POST'])
@login_required # Admin-only
def wish_delete(wish_id):
  wish = Wish.query.get_or_404(wish_id)

  if delete_wish(wish):
    return redirect(url_for('wish.wishes'))

  return redirect(url_for('wish.wishes'))

@wish.route('/toggle/<int:wish_id>', methods=['GET'])
@login_required
def wish_toggle(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  toggle_wish(wish)

  return redirect(url_for('wish.wishes'))

# ADMIN ONLY

# ToDo : Complete
@wish.route('/all/delete', methods=['GET', 'POST'])
@login_required # Admin-only
def wishes_delete():
  return 'wishes_delete'

@wish.route('/all/json', methods=['GET'])
# @login_required
def wishes_json():
  wishes = Wish.query.all()
  wish_list = [wish.to_dict() for wish in wishes]
  return jsonify(wish_list)
