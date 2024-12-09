import os
from flask import Blueprint, current_app, jsonify, send_from_directory
from flask_login import login_required
from ..util.logger import log
from ..wish.model import Wish
from .function import delete_image
from app import db

util = Blueprint('util', __name__, url_prefix='/util', static_folder='.', template_folder='.')

@util.route('/file/save/<path:filename>', methods=['GET'])
@login_required
def upload_file(filename):
  return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@util.route('/file/delete/<int:wish_id>', methods=['GET'])
@login_required
def delete_file(wish_id):
  log.debug(f'Received DELETE request for wish ID: {wish_id}')
  wish = Wish.query.get_or_404(wish_id)

  log.debug(f'wish.image: {wish.image}')

  if wish.image:
    log.debug(f'Deleting image: {wish.image}')
    delete_image(wish.image)
    wish.image = None
    db.session.commit()

    return jsonify(success=True)

  return jsonify(success=False), 404
