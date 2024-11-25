import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for, jsonify
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

def handle_wish_form(form, wish=None):
  """Handle form data for creating or editing a wish."""
  if form.validate_on_submit():
    file = form.img.data if 'img' in form else None

    if file:
      filename = secure_filename(file.filename)
      file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

      try:
        file.save(file_path)
      except Exception as e:
        flash(f'Error saving file: {e}')
        return None

    if wish is None:
      # Creating a new wish
      wish = Wish(
        description=form.description.data,
        url=form.url.data,
        img=filename if file else None,
        owner=current_user
      )
      db.session.add(wish)
    else:
      # Editing an existing wish
      wish.description = form.description.data
      wish.url = form.url.data
      if file:
        wish.img = filename

    db.session.commit()
    flash('Wish saved successfully!')
    return wish

@main.route('/wish', methods=['GET', 'POST'])
@login_required
def wish():
  wishes = Wish.query.filter_by(owner=current_user).all()
  their_wishes = Wish.query.filter(Wish.owner != current_user).all()

  for wish in their_wishes:
    if wish.url:
      parsed_url = urlparse(wish.url)
      wish.domain = parsed_url.hostname

  return render_template('main/wish.htm', wishes=wishes, their_wishes=their_wishes)

@main.route('/create_wish', methods=['GET', 'POST'])
@login_required
def create_wish():
  form = WishForm()
  if request.method == 'POST':
    if handle_wish_form(form):
      return redirect(url_for('main.wish'))
    flash_errors(form)
  return render_template('main/wish_form.htm', form=form, is_edit=False)

@main.route('/edit_wish/<int:wish_id>', methods=['GET', 'POST'])
@login_required
def edit_wish(wish_id):
  wish = Wish.query.get_or_404(wish_id)
  if wish.owner != current_user:
    flash('You can only edit your own wishes.')
    return redirect(url_for('main.wish'))

  form = WishForm(obj=wish)
  if request.method == 'POST':
    if handle_wish_form(form, wish):
      return redirect(url_for('main.wish'))
    flash_errors(form)
  return render_template('main/wish_form.htm', form=form, is_edit=True)

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
  