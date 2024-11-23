from flask import Blueprint

from .index import index as index_blueprint
from .user.route import login as login_blueprint
from .wish.route import wish as wish_blueprint

def register_route(app):
  blueprints = [
    index_blueprint,
    login_blueprint,
    wish_blueprint,
  ]

  for blueprint in blueprints:
    try:
      app.register_blueprint(blueprint)
    except Exception as e:
      app.logger.error(f'Error registering blueprint {blueprint.name}: {e}')
