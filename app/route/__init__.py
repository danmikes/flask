from flask import Blueprint

from .auth import auth as auth_blueprint
from .main import main as main_blueprint

def register_route(app):
  app.register_blueprint(auth_blueprint)
  app.register_blueprint(main_blueprint)
