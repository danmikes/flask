from flask_login import UserMixin
from .. import db

class Wish(db.Model):
  __tablename__ = 'wish'

  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(200), nullable=False)
  url = db.Column(db.String(200), nullable=True)
  img = db.Column(db.String(100), nullable=True)
  bought = db.Column(db.Boolean, default=False)

  buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  buyer = db.relationship('User', back_populates='bought_wishes', foreign_keys=[buyer_id])

  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  owner = db.relationship('User', back_populates='wishes', foreign_keys=[owner_id])

  def __init__(self, description, url, img, owner, buyer=None):
    self.description = description
    self.url = url
    self.img = img
    self.owner = owner
    self.buyer_id = buyer.id if buyer else None
    self.buyer = buyer if buyer else None

  def __repr__(self):
    return '<Wish {self.id}: {self.description[:20]}... - {self.img}>'    

  def to_dict(self):
    return {
      'id': self.id,
      'description': self.description,
      'url': self.url,
      'img': self.img,
      'bought': self.bought,
      'buyer_id': self.buyer_id,
      'buyer': self.buyer.to_dict() if self.buyer else None,
      'owner_id': self.owner_id,
      'owner': self.owner.to_dict(),
    }
