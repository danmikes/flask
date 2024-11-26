import os
from app import create_app, db, log
from app.user import User
from app.wish import Wish
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
  file_path = os.path.join(app.config['UPLOAD_FOLDER'])
  log.debug('File path: {file_path}')

  inspector = inspect(db.engine)
  tables = inspector.get_table_names()
  log.info(f'DataBase Tables: {tables}')

  users = {
    'user1' : User(username='user1', password=generate_password_hash('user1')),
    'user2' : User(username='user2', password=generate_password_hash('user2')),
    'user3' : User(username='user3', password=generate_password_hash('user3')),
  }

  wishes = {
    'wish1' : Wish(description='Test-1', owner=users['user1']),
    'wish2' : Wish(description='Test-2', owner=users['user2'], url='https://perplexity.ai'),
    'wish3' : Wish(description='Test-3', owner=users['user3'], url='https://perplexity.ai', image='brew.png'),
  }

  for user_key, user in users.items():
    db.session.add(user)
    db.session.commit()
    log.info(f'Created Wish: {user.username}')

  for wish_key, wish in wishes.items():
    db.session.add(wish)
    db.session.commit()
    log.info(f'Created Wish: {wish.description}')
