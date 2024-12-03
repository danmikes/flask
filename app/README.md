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
or
```
python -m venv .venv
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
python -m pip install -r pack3.1x.cfg
```
## run
```
flask run --debug
```
or
```
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
or
```
source kill_port.sh
```

# cache
## clean
```
source clean_cache.sh
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
source /home/dmikes/mysite/venv
pip install flask
pip install -r pack.cfg
```
## wsgi.py
```
import sys
path = '/home/dmikes/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

from app import create_app
application = create_app()
```
or?
```
import sys

project_home = '/home/dmikes/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from run import app as application
```
or?
```
import sys
import os

project_home = '/home/dmikes/mysite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

mysite_path = os.path.abspath('/home/dmikes/mysite')
if mysite_path not in sys.path:
    sys.path.insert(0, mysite_path)

import mysite
print(mysite.__file__)

try:
    from mysite.app import create_app
    application = create_app()
except Exception as e:
    print(f'ImportError: {e}')
```
or?
```
import sys

project_home = '/home/dmikes/mysite/app'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from __init__ import app as application  # noqa
```

