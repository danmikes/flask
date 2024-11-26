import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from .util.logger import log

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
  app = Flask(__name__, static_folder='', template_folder='')
  app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'upload')

  app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='top_secret',
  )

  csrf.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)

  with app.app_context():
    from .user.model import User
    from .wish.model import Wish
    try:
      db.create_all()
    except Exception as e:
      log.error(f'Error creating database tables: {e}')

  register_blueprint(app)

  return app

def register_blueprint(app):
  from .blueprint import register_route
  try:
    register_route(app)
  except ImportError as e:
    log.error(f'Error importing blueprint: {e}')

@login_manager.user_loader
def load_user(user_id):
  from .user.model import User
  try:
    return User.query.get(int(user_id))
  except Exception as e:
     log.error(f'Error loading user: {e}')
     return None

@login_manager.unauthorized_handler
def unauthorized():
  return 'Log-In to access this page', 403
