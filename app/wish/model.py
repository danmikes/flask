from sqlalchemy import event
from urllib.parse import urlparse
from .. import db

class Wish(db.Model):
  __tablename__ = 'wish'

  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(200))
  url = db.Column(db.String(200))
  image = db.Column(db.String(100))

  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
  owner = db.relationship('User', back_populates='wishes', foreign_keys=[owner_id])

  buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=True)
  buyer = db.relationship('User', back_populates='wishes_bought', foreign_keys=[buyer_id])

  def __init__(self, description=None, owner=None, url=None, image=None, buyer=None):
    self.description = description
    self.url = url
    self.image = image
    self.owner = owner
  
  @property
  def is_bought(self):
    return self.buyer is not None

  @property
  def domain(self):
    return urlparse(self.url).hostname if self.url else None

  def __repr__(self):
    return f'<Wish {self.id}: {self.description[:20]}... - {self.image} - {self.is_bought}>'

  def to_dict(self):
    return {
      'id': self.id,
      'description': self.description,
      'url': self.url,
      'image': self.image,
      'buyer': self.buyer.to_dict() if self.buyer else None,
      'owner': self.owner.to_dict(),
      'is_bought': self.is_bought,
      'domain': self.domain,
    }

@event.listens_for(Wish.buyer, 'set')
def set_is_bought(target, value, *_):
  target.is_bought = value is not None
