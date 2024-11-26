import os
from flask import Blueprint, current_app
from ..util.logger import log

util = Blueprint('util', __name__)

@util.route('/util/test')
def test():
  file_path = os.path.join(current_app.config['UPLOAD_FOLDER'])
  log.debug(f'File path: {file_path}')

  return 'TEST'

@util.route('/util/log')
def logger():
  log.debug('Debug message')
  log.info('Info message')
  log.warning('Warning message')
  log.error('Error message')
  log.critical('Critical message')
  return 'Logger works!'
