import os
from app import create_app, db, log
from app.user import User
from app.wish import Wish
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
  file_path = os.path.join(app.config['UPLOAD_FOLDER'])
  log.debug(f'File path: {file_path}')

  inspector = inspect(db.engine)
  tables = inspector.get_table_names()
  log.info(f'DataBase Tables: {tables}')

  user_data = [
    {'username': 'user1', 'password': 'user1'},
    {'username': 'user2', 'password': 'user2'},
    {'username': 'user3', 'password': 'user3'},
  ]

  users = []
  for data in user_data:
    user = User(
      username=data['username'],
      password=data['password'],
    )
    users.append(user)
    log.info(f'Prepared user: {user.username}')

  db.session.add_all(users)

  wish_data = [
    {'description': 'Test-1', 'owner': users[0]},
    {'description': 'Test-2', 'owner': users[1], 'url': 'https://perplexity.ai'},
    {'description': 'Test-3', 'owner': users[2], 'url': 'https://perplexity.ai', 'image': 'brew.png'},
  ]

  wishes = []
  for data in wish_data:
    wish = Wish(
      description=data['description'],
      owner=data['owner'],
      ** {k: v for k, v in data.items() if k not in ['description', 'owner']}
    )
    wishes.append(wish)
    log.info(f'Prepared wish: {wish.description}')

  db.session.add_all(wishes)

  db.drop_all()
  db.create_all()
  db.session.commit()
  log.info('All users and wishes created')
