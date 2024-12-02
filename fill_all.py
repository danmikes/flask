import os
from app import create_app, db
from app.user import User
from app.wish import Wish
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
      raise ValueError(f'User {data['owner']} absent')
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
    db.drop_all()
    db.create_all()

    setup_upload_folder(app)
    log_database_tables()

    users = create_users(user_data)
    db.session.add_all(users)
    db.session.flush()

    wishes = create_wishes(wish_data)
    db.session.add_all(wishes)

    db.session.commit()
    log.info('Successfully created users and wishes')
  except Exception as e:
    db.session.rollback()
    log.error(f'Error initialising database: {str(e)}')
  finally:
    db.session.close()

def main():
  app = create_app()
  with app.app_context():

    user_data = [
      {'username': 'user1', 'password': 'user1'},
      {'username': 'user2', 'password': 'user2'},
      {'username': 'user3', 'password': 'user3'},
    ]

    wish_data = [
      {'owner': 'user1', 'description': 'Mini-Oven', 'url': None, 'image': None},
      {'owner': 'user1', 'description': 'Book - Bloodchild & Other Stories', 'url': 'https://www.bol.com/nl/nl/p/bloodchild-other-stories/1001004002579962/?bltgh=iMfoBxXUcZGp0qfSFt9EPA.vOkfDzsqWgwyo4JDFB5N0A_0_16.39.ProductTitle', 'image': 'bloodchild.png'},
      {'owner': 'user1', 'description': 'Pannenkoeken-pan - willekeurig welke, Action/Blokker', 'url': 'https://www.action.com/nl-nl/p/2582341/tefal-crepepan/', 'image': 'pan.png'},
      {'owner': 'user1', 'description': 'Bullet-Journaal', 'url': 'https://www.bol.com/nl/nl/p/mus-bullet-journal-cloudforest/9300000174936833/?Referrer=ADVNLGOO002008J-S--9300000174936833&gad_source=1', 'image': 'journal.png'},
      {'owner': 'user2', 'description': 'Kalender', 'url': 'https://www.bol.com/nl/nl/p/tres-riches-heures-2025-wall-calendar/9300000172511141/?bltgh=qKRAWeusYow9RTzlFiFBdA.2_6.7.ProductImage', 'image': 'calendar.png'},
      {'owner': 'user2', 'description': 'Tracey Chevalier boek "The Glass Maker" => engelstalig', 'url': 'https://www.bol.com/nl/nl/p/the-glassmaker/9300000161834501/?bltgh=g0enH8ErWH5yTD29ZKtLcw.2_6.7.ProductTitle', 'image': 'glassmaker.png'},
      {'owner': 'user2', 'description': 'Merino shirt van JOHA, maat M, donkere kleur', 'url': 'https://www.bergfreunde.nl/joha-womens-t-shirt-merino-ondergoed/', 'image': 'shirt.png'},
      {'owner': 'user2', 'description': 'Merino blouse van JOHA, maat 85/15, donkere kleur', 'url': 'https://www.bergfreunde.nl/joha-womens-blouse-85-15-merino-ondergoed/', 'image': 'blouse.png'},
      {'owner': 'user2', 'description': 'Digitale (of niet) cadeaukaart van Fusion Sport kleding', 'url': 'https://nl.fusionworld.com/products/fusion-giftcard?variant=42874176569495', 'image': 'fusion.png'},
      {'owner': 'user2', 'description': 'Air-Tag', 'url': 'https://www.bol.com/nl/nl/p/lifemate-life-tag-apple-find-my-zoek-mijn-tracker-airtag-bluetooth-tracker-2-pack/9300000193625605/?s2a=&bltgh=rg-V2Qjdh5B9HDFCX85B1g.2_44_45.46.FeatureOptionButton#productTitle', 'image': 'tag.png'},
      {'owner': 'user3', 'description': 'Melkopschuimer Nespresso (kopen op Nespresso)', 'url': 'https://www.nespresso.com/nl/en/order/accessories/original/aeroccino-melkopschuimer-zwart', 'image': 'milk.png'},
      {'owner': 'user3', 'description': 'Merino Thermo Shirt lange mouw - Devold maat L - donker(der)', 'url': 'https://www.bergfreunde.eu/devold-breeze-shirt-merino-base-layer/', 'image': 'devold.png'},
      {'owner': 'user3', 'description': 'Merino Thermo Shirt lange mouw - Engel maat L - donker(der)', 'url': 'https://www.bergfreunde.eu/engel-unterhemd-l-s-merino-base-layer/?cnid=e3869581b6f97e3986facdb502607', 'image': 'engel.png'},
      {'owner': 'user3', 'description': 'iPhone/MacBook Schroevendraaiers: PentaLobe P5 & Torx T5', 'url': 'https://www.borcaden.nl/product/macbook-pro-air-schroevendraaier-set-torx-t5-en-pentalobe/', 'image': 'screw.png'},
      {'owner': 'user3', 'description': 'Rug-krabber', 'url': 'https://www.bol.com/nl/nl/p/rug-scrubber-doucheborstel-lange-lichaamsborstel-dubbelzijdig-design-70cm-rugborstel-krabber-douche-bad-badborstel-rug-krabber-siliconen-massage-borstel-bath-towel-back-scrubber/9300000035988818/?bltgh=uekGctkUynE-iEECuThGFw.2_12.13.ProductTitle', 'image': 'scrub.png'},
      {'owner': 'user3', 'description': 'Bijdrage voor iets', 'url': None, 'image': None},
    ]

    initialise_database(app, user_data, wish_data)

if __name__ == "__main__":
  main()
