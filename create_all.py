from app import create_app, db
from app.util.logger import log

app = create_app()
with app.app_context():
  db.create_all()
  log.info('All tables created.')
