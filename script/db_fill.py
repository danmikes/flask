import os
from app import create_app, db
from app.user.model import User
from app.wish.model import Wish
from sqlalchemy import inspect
from app.util.logger import log

from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
  if isinstance(dbapi_connection, sqlite3.Connection):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA busy_timeout = 60000;")
    cursor.close()

def setup_upload_folder(app):
  upload_folder = app.config['UPLOAD_FOLDER']
  os.makedirs(upload_folder, exist_ok=True)
  log.info(f'Upload folder created: {upload_folder}')

def log_database_tables():
  inspector = inspect(db.engine)
  tables = inspector.get_table_names()
  log.info(f'Database Tables: {tables}')

def create_users(user_data):
  users = []
  for data in user_data:
    user = User(username=data['username'], password=data['password'])
    users.append(user)
    log.info(f'Prepared user: {user.username}')
  return users

def create_wishes(wish_data):
  wishes = []
  users = {user.username: user for user in User.query.all()}
  for data in wish_data:
    owner = users.get(data['owner'])
    if owner is None:
      raise ValueError(f"User {data['owner']} absent")
    wish = Wish(
      owner=owner,
      description=data['description'],
      **{k: v for k, v in data.items() if k not in ['owner', 'description']}
    )
    wishes.append(wish)
    log.info(f'Prepared wish: {wish.description}')
  return wishes

def initialise_database(app, user_data, wish_data):
  try:
    db.session.begin()
    # db.drop_all()
    db.create_all()

    log.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    setup_upload_folder(app)
    log_database_tables()

    users = create_users(user_data)
    db.session.add_all(users)
    db.session.flush()

    wishes = create_wishes(wish_data)
    db.session.add_all(wishes)

    db.session.commit()
    log.info('Created users and wishes')
  except Exception as e:
    db.session.rollback()
    log.error(f'Created no users and wishes: {str(e)}')
    raise
  finally:
    db.session.close()

def main():
  app = create_app()
  with app.app_context():

    user_data = [
      {'username': 'daniel', 'password': 'daniel'},
      {'username': 'brian', 'password': 'brian'},
      {'username': 'cora', 'password': 'cora'},
      {'username': 'jason', 'password': 'jason'},
      {'username': 'karel', 'password': 'karel'},
      {'username': 'kevin', 'password': 'kevin'},
      {'username': 'natalia', 'password': 'natalia'},
      {'username': 'olessia', 'password': 'olessia'},
      {'username': 'richard', 'password': 'richard'},
      {'username': 'valeria', 'password': 'valeria'},
      {'username': 'vera', 'password': 'vera'},
    ]

    wish_data = [
      {'owner': 'daniel', 'description': 'Wish', 'url': None, 'image': None},
    ]

    initialise_database(app, user_data, wish_data)
    log.info(f"Users in DB: {[user.username for user in User.query.all()]}")
    log.info(f"Wishes in DB: {[wish.description for wish in Wish.query.all()]}")

if __name__ == '__main__':
  main()
