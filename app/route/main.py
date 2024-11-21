import os
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
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
    file = None

    if form.img.data:
      file = form.img.data

      if file:
        filename = secure_filename(form.img.data.filename)
        file_path = os.path.join(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        file.save(file_path)

    new_wish = Wish(
      description=form.description.data,
      url=form.url.data,
      img=file_path if file else None,
      owner=current_user
    )

    db.session.add(new_wish)
    db.session.commit()
    flash('Wish added!')

    return redirect(url_for('main.wishlist'))
  
  wishes = Wish.query.filter_by(owner=current_user).all()
  their_wishes = Wish.query.filter(Wish.owner != current_user, Wish.bought == False).all()
  flash_errors(form)

  return render_template('main/wishlist.htm', form=form, wishes=wishes, their_wishes=their_wishes)

@main.route('/wishes')
@login_required
def wishes():
  bought_wishes = Wish.query.filter_by(bought=True).all()

  return render_template('main/wishes.htm', wishes=bought_wishes)

@main.route('/mark_as_bought/<int:wish_id>')
@login_required
def mark_as_bought(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  if wish.owner == current_user:
    flash('You cannot mark your own wish as bought')
    return redirect(url_for('main.wishlist'))
  
  wish.bought = True
  wish.buyer_id = current_user.id
  db.session.commit()
  flash('Wish marked as bought')
  return redirect(url_for('main.wishlist'))
