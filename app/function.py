import json
import os
from flask import redirect, url_for
from flask_assets import Environment, Bundle
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from .util.logger import log

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()

def config_app(app):
  app.config['ADMIN_USERNAME'] = 'daniel'
  app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'upload')
  app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
  os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

  app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI='sqlite:///data.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='top_secret',
  )

def initialise_extensions(app):
  csrf.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)

def initialise_database(app):
  with app.app_context():
    from .user.model import User
    from .wish.model import Wish
    try:
      db.create_all()
    except Exception as e:
      log.error(f'Error creating database tables: {e}')

def register_blueprints(app):
  from .blueprint import register_route
  try:
    register_route(app)
  except ImportError as e:
    log.error(f'Error importing blueprint: {e}')

def build_assets(app):
  assets = Environment(app)

  scss = Bundle('style.css',
                'color.scss',
                filters='libsass',
                output='all.css',
                depends='*.scss')
  assets.register("asset_css", scss)
  scss.build()

def load_content(lang):
  file_path = os.path.join('app/content', f'{lang}.json')

  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      return json.load(f)
  except FileNotFoundError:
    log.error(f'Content file not found: {file_path}')
    return {}

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
  return redirect(url_for('user.user_login'))
