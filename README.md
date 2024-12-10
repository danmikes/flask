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
https://eu.pythonanywhere.com/user/dmikes/<flask>
<flask> is project folder
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
## github-action
```
Add webhook.yml as GitHub-action
```
## webhook-listener
```
Add webhook-listener.py to PythonAnyWhere <flask>
```
## wsgi.py
```
Upload wsgi.py to PythonAnyWhere <flask>
```
## url
```
Enjoy the app : https://dmikes.eu.pythonanywhere.com
```
