from flask import Blueprint, render_template

index = Blueprint('main', __name__)

@index.route('/')
def index():
  return render_template('index.htm')
