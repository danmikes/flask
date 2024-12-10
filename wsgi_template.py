import sys
import os
from flask import Flask

path = '/home/dmikes/flask'
if path not in sys.path:
  sys.path.append(path)

from app import create_app

flask_app = create_app()

from webhook_listener import webhook_app

def wsgi_application(environ, start_response):
  if environ['PATH_INFO'].startswith('/update_server'):
    return webhook_app(environ, start_response)
  return flask_app(environ, start_response)

application = wsgi_application
