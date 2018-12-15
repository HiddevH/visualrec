
## Documentation on how to use docker in combination with Google App Engine.

In your google cloud shell create the following structure:

```
.
├── app
│   ├── main.py
│   └── static
│       └── index.html
├── Dockerfile
└── app.yaml
```

Example codes:
```
mkdir project
cd project
mkdir app
mkdir app/static
```

main.py

```
cat > app/main.py <<EOF
import os
from flask import Flask, send_file
app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World from Flask"

@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, 'index.html')
    return send_file(index_path)

# Everything not declared before (not a Flask route / API endpoint)...
@app.route('/<path:path>')
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        return send_file(index_path)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=8080)
EOF
```

index.html
```
cat > app/static/index.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Index</title>
</head>
<body>
<h1>Hello World from HTML</h1>
</body>
</html>
EOF
```

app.yaml
```
cat > app.yaml <<EOF
runtime: custom
env: flex
EOF
```

Dockerfile
```
cat > Dockerfile <<EOF
FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV STATIC_INDEX 1

COPY ./app /app
EOF
```



Run the following to build an image. 

```
docker build -t myimage .
docker rm mycontainer
docker run -d --name mycontainer -p 8080:8080 myimage

#If IP port already occupied do 1 of the following:
sudo netstat -peanut 
sudo netstat -ntpl | grep 8080

#Last number is the PID #, then do:
sudo kill PID

gcloud app create
gcloud app deploy
gcloud app browse
```


virtualenv --python python3 venv
source venv/bin/activate
In main project folder: 

mkdir lib

pip install -t lib/ <library_name>

Create file appengine_config.py in the same as app.yaml 

```
cat > appengine_config.py <<EOF
# appengine_config.py
from google.appengine.ext import vendor

# Add any libraries install in the "lib" folder.
vendor.add('lib')
EOF
```

Create requirements.txt file in main folder

```
cat > requirements.txt <<EOF
click==6.7
cmake==3.12.0
dlib==19.15.0
dominate==2.3.4
face-recognition==1.2.3
face-recognition-models==0.3.0
Flask==1.0.2
Flask-Bootstrap==3.3.7.1
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
numpy==1.15.1
Pillow==5.2.0
uWSGI==2.0.17.1
visitor==0.1.3
Werkzeug==0.14.1
EOF
```

pip install -t lib -r requirements.txt




Old code for python: 



```
cat > main.py <<EOF

# [START gae_python37_app]
from flask import Flask

# If entrypoint is not defined in app.yaml, App Engine will look for an app
# called app in main.py.
app = Flask(__name__)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an entrypoint to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
EOF

cat > main_test.py <<EOF

import main
def test_index():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert 'Hello World' in r.data.decode('utf-8')
EOF

cat > app.yaml << EOF
runtime: python37
EOF

virtualenv --python python3 ~/envs/hello_world
source ~/envs/hello_world/bin/activate
pip install -r requirements.txt
python main.py
gcloud app deploy app.yaml--project project amazing-blend-217212
gcloud app browse
gcloud app logs tail -s default
https://amazing-blend-217212.appspot.com/
```
