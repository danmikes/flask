import os
from flask import Blueprint, current_app, send_from_directory
from flask_login import login_required
from ..util.logger import log
from .function import remove_unused_files

util = Blueprint('util', __name__, url_prefix='/util', static_folder='.', template_folder='.')

@util.route('/upload/<path:filename>')
@login_required
def upload_file(filename):
  return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@util.route('/upload/remove_unused')
@login_required
def test():
  deleted_count = remove_unused_files()
  return f'Removed unused files: {deleted_count}'
