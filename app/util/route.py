import os
from flask import Blueprint, current_app

util = Blueprint('util', __name__)

@util.route('/util/test')
def test():
  file_path = os.path.join(current_app.config['UPLOAD_FOLDER'])
  print(f'File path: {file_path}')

  return 'TEST'
