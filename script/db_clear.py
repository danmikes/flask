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

def log_database_tables():
  inspector = inspect(db.engine)
  tables = inspector.get_table_names()
  log.info(f'Database Tables: {tables}')

def drop_all_data():
  try:
    num_wishes_deleted = db.session.query(Wish).delete()
    num_users_deleted = db.session.query(User).delete()
    db.session.commit()
    log.info(f'Deleted {num_users_deleted} users and {num_wishes_deleted} wishes')
  except Exception as e:
    db.session.rollback()
    log.error(f'Deleted no users and wishes: {str(e)}')
    raise
  finally:
    db.session.close()

def main():
  app = create_app()
  with app.app_context():
    log.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    log_database_tables()

    log.info(f"Users in DB before: {[user.username for user in User.query.all()]}")
    log.info(f"Wishes in DB before: {[wish.description for wish in Wish.query.all()]}")

    drop_all_data()

    log.info(f"Users in DB after: {[user.username for user in User.query.all()]}")
    log.info(f"Wishes in DB after: {[wish.description for wish in Wish.query.all()]}")

if __name__ == '__main__':
  main()
