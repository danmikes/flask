import sys

from app import create_app
application = create_app()

path = '/home/dmikes/flask'
if path not in sys.path:
  sys.path.append(path)
