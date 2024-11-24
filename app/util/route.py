from flask import Blueprint, jsonify
from flask_wtf.csrf import generate_csrf
import requests
from sqlalchemy import text
from .. import db

util = Blueprint('util', __name__)

@util.route('/test')
def test():
  return 'TEST'
