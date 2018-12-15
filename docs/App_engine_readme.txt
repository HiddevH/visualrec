
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
