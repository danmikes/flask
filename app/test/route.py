from flask import Blueprint
from ..util.logger import log

tst = Blueprint('tst', __name__, url_prefix='/test', static_folder='.', template_folder='.')

@tst.route('/')
def test():
  return 'test'
