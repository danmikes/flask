import os
from flask import Blueprint, current_app, send_from_directory
from ..util.logger import log

util = Blueprint('util', __name__, url_prefix='/util', static_folder='.', template_folder='.')

@util.route('/test')
def test():
  file_path = os.path.join(current_app.config['UPLOAD_FOLDER'])

  return file_path
