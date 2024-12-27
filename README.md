# Wish-App
This app manages wishes for family.

Written with Flask Python Jinja Bulma.

Virtual Environment created with `pythonV -m venv .venv`
- PythonV
  - python (unversioned)
  - python3.13
  - python3.10

Libraries installed with `pythonV -m pip install -r pack.txt`
- pythonV / pack
  - python (unversioned) : pack.txt
  - python3.13 : pack3.13.txt
  - python3.10 : pack3.10.txt (PythonAnyWhere)

Deployed with GitHub PythonAnyWhere GitHub-action WebHook-listener.

# python
## install
```
brew install python pip
```

# virtual environment
## create
```
python -m venv .venv
```
## activate
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
python -m pip install -r pack.txt
```
## run
```
flask run --debug
```
## map
```
python map.py
```

# database
## reset
```
python reset_db.py
```

# port
## kill
```
source kill_port.sh
```

# cache
## clear
```
source clear_cache.sh
```

# git
## fresh start
```
git branch new_branch_name $(echo "commit message" | git commit-tree HEAD^{tree})
git reset --hard origin/main
```

# test
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
## site
```
https://eu.pythonanywhere.com/user/dmikes/<flask>
<flask> is project folder
/home/dmikes/flask/
```
## git
```
git clone github.com/dmikes/flask
```
## venv
```
deactivate
rm -rf .venv
python3.10 -m venv .venv
source .venv/bin/activate
pip install flask
pip install -r pack<3.1x>.txt
```
## wsgi.py
```
Upload wsgi.py to PythonAnyWhere <flask>
```
## url
```
Enjoy the app : https://dmikes.eu.pythonanywhere.com
```

# deploy-global - pi
## site
```
https://dmikes.hopto.org
/home/pi/flask/
```
## git
```
git clone github.com/dmikes/flask
```
## venv
```
deactivate
rm -rf .venv
python3.10 -m venv .venv
source .venv/bin/activate
pip install flask
pip install -r pack<3.1x>.txt
```
## gunicorn
```
pip install gunicorn
```
## nginx
```
sudo apt install nginx
```
## site
```
flask.conf -> /etc/nginx/sites-available/flask.conf
sudo ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/
```
## system
```
flask.socket -> /etc/systemd/system/flask.socket
flask.service -> /etc/systemd/system/uwsgi.service
```
## router
```
port 80 -> pi
port 443 -> pi
```
## cert
```
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d dmikes.hopto.org
max8@post.cz
http -> https
renewal automatic
```
## update
```
sudo nginx -t
```
## curl
```
curl -svo /dev/null https://dmikes.hopto.org
```
## url
```
Enjoy the app : https://dmikes.hopto.org
```
## apparmor
```
sudo aa-complain /usr/sbin/nginx
sudo aa-enforce /usr/sbin/nginx
```
## flask
```
./enable.sh
./start.sh
./restart.sh
./status.sh
```
