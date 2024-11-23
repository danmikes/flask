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
  wish_id = request.args.get('wish_id', type=int)
  if wish_id:
    wish = Wish.query.get_or_404(wish_id)
    if wish.owner != current_user:
      flash('You can only edit your wishes', 'error')
      return redirect(url_for('main.wishes'))
  else:
    wish = Wish(description='', url='', image='', owner=current_user)

  form = WishForm(obj=wish)

  if form.validate_on_submit():
    if not wish_id:
      wish = Wish(owner=current_user)

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
        return redirect(url_for('main.wish'))

    if not wish.id:
      db.session.add(wish)

    db.session.commit()
    flash('Wish saved', 'success')
    return redirect(url_for('main.wishes'))

  return render_template('unit/form.htm', form=form)

@main.route('/wishes', methods=['GET'])
@login_required
def wishes():
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

  return render_template('main/wishes.htm', users=users, wishes_by_user=wishes_by_user)

@main.route('/buy/<int:wish_id>')
@login_required
def buy(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  if wish.owner_id == current_user.id:
    flash('You cannot buy your own wish', 'error')
    return redirect(url_for('main.wishes'))
  
  wish.bought = True
  wish.buyer_id = current_user.id
  db.session.commit()
  flash('Wish marked as bought', 'success')
  return redirect(url_for('main.wishes'))

@main.route('/cancel/<int:wish_id>')
@login_required
def cancel(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  
  wish.bought = False
  wish.buyer_id = None
  db.session.commit()
  flash('Wish canceled', 'success')
  return redirect(url_for('main.wishes'))

@main.route('/wishes/json', methods=['GET'])
@login_required
def wishes_json():
  wishes = Wish.query.all()
  wish_list = [wish.to_dict() for wish in wishes]
  return jsonify(wish_list)
