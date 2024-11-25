from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

class User(UserMixin, db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True)
  password_hash = db.Column(db.String(128))
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)

  wishes = db.relationship('Wish', back_populates='owner')
  wishes_bought = db.relationship('Wish', back_populates='buyer')

  def __init__(self, username, password):
    self.username = username
    self.set_password(password)

  def __repr__(self):
    return '<User {self.id}: {self.username}>'
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def to_dict(self):
    return {
      'id': self.id,
      'username': self.username,
      'timestamp': self.timestamp,
      'wishes': self.wishes,
      'wishes_bought': self.wishes_bought,
      'is_match': self.check_password(self.username)
    }
