from flask import Blueprint

from .route import base
from .user.route import user
from .util.route import util
from .wish.route import wish

def register_route(app):
  blueprints = [
    base,
    user,
    util,
    wish,
  ]

  for blueprint in blueprints:
    try:
      app.register_blueprint(blueprint)
    except Exception as e:
      app.logger.error(f'Error registering blueprint {blueprint.name}: {e}')
