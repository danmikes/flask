import os
from app import create_app, db, log
from app.user import User
from app.wish import Wish
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
  upload_folder = app.config['UPLOAD_FOLDER']
  os.makedirs(upload_folder, exist_ok=True)

  log.debug(f'Upload folder: {upload_folder}')

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

  image_filenames = [
    'image1.png',
    'image2.png',
    'image3.png',
  ]
  for filename in image_filenames:
    with open(os.path.join(upload_folder, filename), 'w') as f:
      f.write('Test file')

  wish_data = [
    {'description': 'Test-1', 'owner': users[0]},
    {'description': 'Test-2', 'owner': users[0], 'url': 'https://bol.com'},
    {'description': 'Test-3', 'owner': users[0], 'url': 'https://blokker.nl', 'image': image_filenames[0]},
    {'description': 'Test-4', 'owner': users[1]},
    {'description': 'Test-5', 'owner': users[1], 'url': 'https://gamma.nl'},
    {'description': 'Test-6', 'owner': users[1], 'url': 'https://praxis.nl', 'image': image_filenames[1]},
    {'description': 'Test-7', 'owner': users[2]},
    {'description': 'Test-8', 'owner': users[2], 'url': 'https://bergfreunde.nl'},
    {'description': 'Test-9', 'owner': users[2], 'url': 'https://decathlon.nl', 'image': image_filenames[2]},
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
