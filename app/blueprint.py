from flask import Blueprint

from .route import base as base_blueprint
from .user.route import user as user_blueprint
from .wish.route import wish as wish_blueprint

def register_route(app):
  blueprints = [
    base_blueprint,
    user_blueprint,
    wish_blueprint,
  ]

  for blueprint in blueprints:
    try:
      app.register_blueprint(blueprint)
    except Exception as e:
      app.logger.error(f'Error registering blueprint {blueprint.name}: {e}')
