import os
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from ..form.wish import WishForm
from ..model.wish import Wish
from ..util.util import flash_errors
from .. import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('main/index.htm')

@main.route('/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist():
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
        return redirect(url_for('main.wishlist'))

    new_wish = Wish(
      description=form.description.data,
      url=form.url.data,
      img=filename if file else None,
      owner=current_user
    )

    db.session.add(new_wish)
    db.session.commit()
    flash('Wish added!')

    return redirect(url_for('main.wishlist'))
  
  wishes = Wish.query.filter_by(owner=current_user).all()
  their_wishes = Wish.query.filter(Wish.owner != current_user).all()

  for wish in their_wishes:
    if wish.url:
      parsed_url = urlparse(wish.url)
      wish.domain = parsed_url.hostname

  flash_errors(form)

  return render_template('main/wishlist.htm', form=form, wishes=wishes, their_wishes=their_wishes)

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
    return redirect(url_for('main.wishlist'))
  
  wish.bought = True
  wish.buyer_id = current_user.id
  db.session.commit()
  flash('Wish marked as bought')
  return redirect(url_for('main.wishlist'))

@main.route('/unmark_as_bought/<int:wish_id>')
@login_required
def unmark_as_bought(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  
  wish.bought = False
  wish.buyer_id = None
  db.session.commit()
  flash('Wish unmarked as bought')
  return redirect(url_for('main.wishlist'))
