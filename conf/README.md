# python

## install
```
brew install python
```

# virtual environment

## create
```
python -m venv venv
```

## activate
```
source venv/bin/activate
```

## deactivate
```
deactivate
```

# flask

## install
```
python -m pip install -r conf/pack.txt
```

## run
```
flask run --debug
```

# git

## fresh start
```
git branch new_branch_name $(echo "commit message" | git commit-tree HEAD^{tree})
git reset --hard origin/main
```

# run
```
flask run --debug
```

# deploy-local

## self
```
flask run --host=0.0.0.0
```

## one
```
<IP-address>
http://192.168.2.26:5000
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

## project
```
https://eu.pythonanywhere.com/user/dmikes/flask
```

## git
```
git clone github.com/danmikes/flask.git
```

## venv
```
deactivate
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate
pip install flask
pip install -r pack3.10.txt
```

## wsgi.py
```
wsgi.py -> /var/www/dmikes_eu_pythonanywhere_com_wsgi.py
```

## webhook
```
webhook.txt -> github.webhook
curl -X POST -H "Content-Type: application/json" -d '{"payload":"test"}' https://dmikes.eu.pythonanywhere.com/util/update
```

## web
```
Wishing Well : https://dmikes.eu.pythonanywhere.com
```
