# Wish-App

- Manages wishes for family
- Uses Flask Python Jinja Bulma

## GitHub
- Repository : https://github.com/danmikes/flask.git
- WebHook : webhook.txt

## Configuration

### PythonAnyWhere
  - Virtual Environment : `python3.10 -m venv .venv`
  - Library : `python3.10 -m pip install -r conf/pack3.10.txt`
  - Proxy-Server : `uWSGI`
  - URL : `https://dmikes.eu.pythonanywhere.com`
  - Configuration : `wsgi.py`

### RaspBerryPi
  - Virtual Environment : `python3.13 -m venv .venv`
  - Library : `python -m pip install -r conf/pack3.13.txt`
  - Proxy-Server: `Gunicorn`
  - URL : `https://dmikes.hopto.org`
  - Configuration : `flask.conf flask.service flask.socket`
