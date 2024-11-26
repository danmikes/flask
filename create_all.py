from app import create_app, db

app = create_app()
with app.app_context():
  db.create_all()
  app.logger.info('All tables created.')
