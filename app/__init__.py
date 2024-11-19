from flask import Flask, current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import logging

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
  app = Flask(__name__, template_folder='template')

  logging.basicConfig(level=logging.DEBUG)
  app.logger.setLevel(logging.DEBUG)

  app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='top_secret',
  )

  csrf.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)

  with app.app_context():
    try:
      db.create_all()
    except Exception as e:
      app.logger.error(f'Error creating database tables: {e}')

  try:
    register_blueprint(app)
  except Exception as e:
    app.logger.error(f'Error registering blueprint: {e}')

  return app

def register_blueprint(app):
  try:
    from .route import main
    return app.register_blueprint(main)
  except ImportError as e:
    app.logger.error(f'Error importing blueprint: {e}')
  except Exception as e:
    app.logger.error(f'Error registering blueprint: {e}')

@login_manager.user_loader
def load_user(user_id):
   try:
    from .model import User
    return User.query.get(int(user_id))
   except Exception as e:
     current_app.logger.error(f'Error loading user: {e}')
     return None

@login_manager.unauthorized_handler
def unauthorized():
  return 'Log In to access this page', 403
