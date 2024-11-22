# python
## install
```
brew install python pip pyenv
```
or
```
. python.sh
```

# virtual environment
## create
```
CMD-SHT-P > Create Environment > PythonX > .venv
```
## activate
```
CMD-SHT-P > Select Environment > PythonX
```
or
```
source .venv/bin/activate
```
## deactivate
```
deactivate
```

# flask
## install
```
python -m pip install flask flask-login flask-sqlalchemy
```
or
```
python -m pip install -r pack.cfg
```
## run
```
flask run --debug
```
## map
```
$ python
>>> from app import app
>>> app.url_map
```

# database
## create
```
python
>>> from app import app, db
>>> app.app_context().push()
>>> app.create_all()
