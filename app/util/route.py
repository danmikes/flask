import os
from flask import Blueprint, current_app, send_from_directory
from ..util.logger import log

util = Blueprint('util', __name__, url_prefix='/util', static_folder='.', template_folder='.')

@util.route('/upload/<path:filename>')
def upload_file(filename):
  return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
