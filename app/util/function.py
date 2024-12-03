import os
from flask import current_app
from ..util.logger import log
from ..wish.model import Wish

def remove_unused_files(app=None):
  if app is None:
    app = current_app

  with app.app_context():
    folder_upload = current_app.config['UPLOAD_FOLDER']
    files_upload = set(os.listdir(folder_upload))

    wish_images = set(os.path.basename(wish.image) for wish in Wish.query.all() if wish.image)
    files_to_delete = files_upload - wish_images
    log.info(f'Files to delete: {files_to_delete}')

    for file_name in files_to_delete:
      file_path = os.path.join(folder_upload, file_name)
      try:
        os.remove(file_path)
        log.info(f'File removed: {file_name}')
      except Exception as e:
        log.info(f'File not removed: {file_name}: {e}')

  return len(files_to_delete)
