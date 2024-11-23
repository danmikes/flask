from flask import Blueprint, render_template

base = Blueprint('base', __name__, template_folder='.')

@base.route('/')
def index():
  return render_template('index.htm')
