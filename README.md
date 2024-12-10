# python
## install
```
brew install python pip pyenv
or
. python.sh
```

# virtual environment
## create
```
CMD-SHT-P > Create Environment > PythonX > .venv
or
python -m venv .venv
or
python3.10 -m venv .venv
or
python3.13 -m venv .venv
```
## activate
```
CMD-SHT-P > Select Environment > PythonX
or
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
or
python -m pip install -r pack3.1x.cfg
```
## run
```
flask run --debug
or
. run
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
or
python create_table.py
```
## drop
```
python
>>> from app import app, db
>>> app.app_context().push()
>>> app.drop_all()
or
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
or
source kill_port.sh
```

# cache
## clean
```
source clear_cache.sh
```

# git
## fresh start
```
git branch new_branch_name $(echo "commit message" | git commit-tree HEAD^{tree})
git reset --hard origin/main
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

# deploy-regional - pyngrok
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

# deploy-global - python-anywhere
##
```
https://eu.pythonanywhere.com/user/dmikes
```
## venv replace
```
deactivate
rm -rf .venv
python3.10 -m venv .venv
source .venv/bin/activate
```
## upload
```
upload app
python3 -m venv /home/dmikes/mysite/venv
source /home/dmikes/mysite/venv/bib/activate
pip install flask
pip install -r pack<3.1x>.txt
```
## wsgi.py
```
upload
```
## url
```
https://dmikes.eu.pythonanywhere.com
```
## webhook
```
upload
```
