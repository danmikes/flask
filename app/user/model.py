from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

class User(UserMixin, db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  # email = db.Column(db.String(30), nullable=False, unique=True)
  username = db.Column(db.String(20), nullable=False, unique=True)
  password_hash = db.Column(db.String(20), nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)

  wishes = db.relationship('Wish', back_populates='owner', foreign_keys='Wish.owner_id')
  bought_wishes = db.relationship('Wish', back_populates='buyer', foreign_keys='Wish.buyer_id')

  def __repr__(self):
    return '<User {self.id}: {self.username} - {self.email}>'
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def to_dict(self):
    return {
      'id': self.id,
      'username': self.username,
      # 'email': self.email,
    }
