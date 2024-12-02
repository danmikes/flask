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
python -m pip install flask flask-login flask-sqlalchemy sas Werkzeug==2.2.2
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
```
or
```
python create_table.py
```
## drop
```
python
>>> from app import app, db
>>> app.app_context().push()
>>> app.drop_all()
```
or
```
python drop_table.py
```

# test
## create
```
python test.py
```

# port
## kill
```
sudo kill -9 $(lsof -t -i:5000 -sTCP:LISTEN)
```

```
python drop_all.py
python create_all.py
python fill_all.sh
source clean_cache.sh or ./clean_cache
source kill_port.sh or ./kill_port.sh
bash run or . run
```

# git
## fresh start
```
git branch new_branch_name $(echo "commit message" | git commit-tree HEAD^{tree})
```

# deploy-local
## self
```
flask run --host=0.0.0.0
```
## one
```
http://<MY_IP_ADDRESS>:5000
```

# deploy-regional
## self
```
pip install pyngrok
flask run --host=0.0.0.0
ngrok http 5000
```
## one
```
<PUBLIC_URL>
e.g. http://abcd1234.ngrok.io
```

# deploy-global
```
python-anywhere
heroku
github
```
