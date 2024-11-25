import os
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from ..user.model import User
from .form import WishForm
from .model import Wish
from ..util.flash import flash_errors
from .. import db

wish = Blueprint('wish', __name__, static_folder='', template_folder='')

def form_validate(form, wish=None):
  if form.validate_on_submit():

    form.populate_obj(wish)

    file = form.image.data
    if file:
      filename = secure_filename(file.filename)
      file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

      try:
        file.save(file_path)
        wish.image = filename
      except Exception as e:
        flash(f'Error saving file: {e}', 'error')
        return redirect(url_for('wish.wish_edit'), wish_id=wish.id)

@wish.route('/wish/new', methods=['GET', 'POST'])
@login_required
def wish_new():
  form = WishForm()
  if form_validate(form):
    db.session.add(wish)
    db.session.commit()
    flash('Wish saved', 'success')
    return redirect(url_for('wish.wishes'))
  
  return render_template('/wish/form.htm', form=form)

@wish.route('/wish/edit/<int:wish_id', methods=['GET', 'POST'])
@login_required
def wish_edit(wish_id):
  wish = Wish.query.get_or_404(wish_id)

  form = WishForm(obj=wish)
  if form_validate(form, wish):
    db.session.commit()
    flash('Wish saved', 'success')
    return redirect(url_for('wish.wishes'))
  
  return render_template('/wish/form.htm', form=form, wish=wish)

@wish.route('/wish/buy/<int:wish_id>')
@login_required
def wish_buy(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  
  wish.buyer = current_user

  db.session.commit()
  flash('Wish bought', 'success')

  return redirect(url_for('wish.wishes'))

@wish.route('/wish/cancel/<int:wish_id>')
@login_required
def cancel(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  
  wish.buyer = None
  db.session.commit()
  flash('Wish canceled', 'success')

  return redirect(url_for('wish.wishes'))

@wish.route('/wishes', methods=['GET'])
@login_required
def wishes():
  users = User.query.all()
  wishes = Wish.query.all()
  wishes_by_user = {}

  for wish in wishes:
    if wish.url:
      parsed_url = urlparse(wish.url)
      wish.domain = parsed_url.hostname

    if wish.owner.id not in wishes_by_user:
      wishes_by_user[wish.owner_id] = []
    
    wishes_by_user[wish.owner_id].append(wish)

  return render_template('wish/view.htm', users=users, wishes_by_user=wishes_by_user)

@wish.route('/wishes/json', methods=['GET'])
# @login_required
def wishes_json():
  wishes = Wish.query.all()
  wish_list = [wish.to_dict() for wish in wishes]
  return jsonify(wish_list)
