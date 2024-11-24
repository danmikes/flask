from flask_login import UserMixin
from .. import db

class Wish(db.Model):
  __tablename__ = 'wish'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  description = db.Column(db.String(200), nullable=False)
  url = db.Column(db.String(200), nullable=True)
  image = db.Column(db.String(100), nullable=True)
  is_bought = db.Column(db.Boolean, default=False)

  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
  owner = db.relationship('User', back_populates='wishes', foreign_keys=[owner_id])

  buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=True)
  buyer = db.relationship('User', back_populates='bought_wishes', foreign_keys=[buyer_id])

  def __init__(self, description, owner, url=None, image=None, buyer=None):
    self.description = description
    self.url = url
    self.image = image
    self.owner = owner

  def __repr__(self):
    return f'<Wish {self.id}: {self.description[:20]}... - {self.image} - {self.is_bought}>'

  def to_dict(self):
    return {
      'id': self.id,
      'description': self.description,
      'url': self.url,
      'image': self.image,
      'is_bought': self.is_bought,
      'buyer': self.buyer.to_dict() if self.buyer else None,
      'owner': self.owner.to_dict(),
    }
