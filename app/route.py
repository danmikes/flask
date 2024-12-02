from flask import Blueprint, render_template

base = Blueprint('base', __name__, url_prefix='/', static_folder='.', template_folder='.')

@base.route('/')
def index():
  return render_template('index.htm')
