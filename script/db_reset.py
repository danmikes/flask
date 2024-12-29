from app import app, db

with app.app_context():
  db.drop_all()
  print("Tables dropped")
  db.create_all()
  print("Tables created")
