from flask import Flask, current_app
from .function import config_app, initialise_extensions, initialise_database, register_blueprints
from .function import db

def create_app():
  app = Flask(__name__, static_folder='/', template_folder='/')

  @app.context_processor
  def inject_admin_username():
    return dict(ADMIN_USERNAME=current_app.config['ADMIN_USERNAME'])

  config_app(app)
  initialise_extensions(app)
  initialise_database(app)
  register_blueprints(app)

  return app
