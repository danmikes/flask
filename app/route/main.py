import os
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from ..model.user import User
from ..form.wish import WishForm
from ..model.wish import Wish
from ..util.util import flash_errors
from .. import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('main/index.htm')

@main.route('/wish', methods=['GET', 'POST'])
@login_required
def wish():
  form = WishForm()

  if form.validate_on_submit():
    file = form.img.data

    if file:
      filename = secure_filename(file.filename)
      file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

      try:
        file.save(file_path)
      except Exception as e:
        flash(f'Error saving file: {e}')
        return redirect(url_for('main.wish'))

    new_wish = Wish(
      description=form.description.data,
      url=form.url.data,
      img=filename if file else None,
      owner=current_user
    )

    db.session.add(new_wish)
    db.session.commit()
    flash('Wish added!')

    return redirect(url_for('main.wish'))

  users = User.query.all()
  wishes = Wish.query.all()
  wishes_by_user = {}
  for wish in wishes:
    if wish.url:
      parsed_url = urlparse(wish.url)
      wish.domain = parsed_url.hostname

    if wish.owner_id not in wishes_by_user:
      wishes_by_user[wish.owner_id] = []
    
    wishes_by_user[wish.owner_id].append(wish)

  flash_errors(form)

  return render_template('main/wish.htm', form=form, users=users, wishes_by_user=wishes_by_user)

@main.route('/wishes')
@login_required
def wishes():
  wishes = Wish.query.all()

  return render_template('main/wishes.htm', wishes=wishes)

@main.route('/mark_as_bought/<int:wish_id>')
@login_required
def mark_as_bought(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  if wish.owner_id == current_user.id:
    flash('You cannot mark your own wish as bought')
    return redirect(url_for('main.wish'))
  
  wish.bought = True
  wish.buyer_id = current_user.id
  db.session.commit()
  flash('Wish marked as bought')
  return redirect(url_for('main.wish'))

@main.route('/unmark_as_bought/<int:wish_id>')
@login_required
def unmark_as_bought(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  
  wish.bought = False
  wish.buyer_id = None
  db.session.commit()
  flash('Wish unmarked as bought')
  return redirect(url_for('main.wish'))

@main.route('/edit_wish/<int:wish_id>', methods=['GET', 'POST'])
def edit_wish(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  form = WishForm()

  if request.method == 'GET':
    form.description.data = wish.description
    form.url.data = wish.url

  if request.method == 'POST':
    if form.validate_on_submit():
      wish.description = form.description.data
      wish.url = form.url.data

      file = request.files.get('img')
      if file:
        filename = secure_filename(file.filename)
        file_path = os.path.joing(current_app.config['UPLOAD_FOLDER'], filename)
        try:
          file.save(file_path)
          wish.img = filename
        except Exception as e:
          flash(f'Error saving file: {e}')
          return redirect(url_for('main.wish'))

      db.session.commit()
      flash('Wish updated successfully!')
      return redirect(url_for('main.wish'))
  
  form.description.data = wish.description
  form.url.data = wish.url

  return render_template('main/wish.htm', form=form, is_edit=True)

@main.route('/wishlist', methods=['GET'])
@login_required
def wishlist():
  wishes = Wish.query.all()
  wish_list = [wish.to_dict() for wish in wishes]
  return jsonify(wish_list)
