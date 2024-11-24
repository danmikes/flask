import os
import time
from flask import Blueprint, current_app

util = Blueprint('util', __name__)

@util.route('/util/test')
def test():
  file_path = os.path.join(current_app.config['UPLOAD_FOLDER'])
  print(f'File path: {file_path}')

  return 'TEST'

@util.route('/util/clean-cache')
def cleanup_cache(cache_dir, max_age=60): # seconds
  current_time = time.time()
  for filename in os.listdir(cache_dir):
    file_path = os.path.join(cache_dir, filename)
    if os.path.isfile(file_path):
      file_age = current_time - os.path.getmtime(file_path)
      if file_age > max_age:
        os.remove(file_path)
        print(f'Removed old cache file: {file_path}')
