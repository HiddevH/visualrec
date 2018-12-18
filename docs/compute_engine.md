---
title: "Flask App for Facial Recognition"
output: html_document
---

## Introduction
This readme is for a project focused on using facial recognition in a python/flask app.
We use a compute engine with python 3.7 and flask for the app, gunicorn for the wsgi server and nginx as web server. For the general explanation of these terms please check Appendix I at the bottom.

### Component and relevant file overview
Here an overview of the main components and relevant files.

```

Load Balancer node
    To be added


Serving Node(s)
    
    Nginx - Web server for receiving external requests from visitors
    /etc/nginx/sites-available/default                                          -- links from external URL to internal ports
    /etc/nginx/sites-enabled/default                                            -- file that is system linked to sites available, never edit this.
    /etc/nginx/nginx.conf                                                       -- nginx settings.
    /etc/nginx/proxy_params                                                     -- standard parameters mapping for nginx to gunicorn communication
    /var/log/nginx/error.log                                                    -- check which errors were served to the visitors/in nginx 
    /var/log/nginx/access.log                                                   -- check which users visited website
    
    Gunicorn - Internal server that starts up a flask app per visitor.
    /etc/systemd/system/main.service                                            -- service that keeps Gunicorn server running
    ~/face_rec/flask/main.socket                                                -- connection tunnel between Gunicorn and Flask
    
    Flask app - The actual Python3.7 based application
    ~/face_rec/flask/wsgi.py                                                    -- tells Gunicorn server how to interact with the application
    ~/face_rec/flask/main.py                                                    -- starts up flask app
        ~/face_rec/flask/face_compare.py                                        -- subscript
        ~/face_rec/flask/create_encodings.py                                    -- subscript
        ~/face_rec/flask/browse_casts.py                                        -- subscript
    
    Virtual Environment - Contains the required packages
    ~/face_rec/flask/venv
    
    Web Content - Content to be served on website
    ~/face_rec/flask/static
    ~/face_rec/flask/templates
```

### Managing and testing the VM

Go to website URL/IP: http://35.246.113.78

HTML/JS/CSS
```
Check in page source if there are errors with the content 
To do: add tests. 

```

Nginx
```
If you encounter any errors on the website, try checking the following:
sudo less /var/log/nginx/error.log : checks the Nginx error logs.
sudo less /var/log/nginx/access.log : checks the Nginx access logs.
sudo systemctl status nginx  : checks the Nginx process logs.
sudo systemctl start/stop/restart nginx  : to start server again.

# check nginx conf file
sudo nano /etc/nginx/nginx.conf

# check port forwarding file
sudo nano /etc/nginx/sites-available/default

# test syntax of file
sudo nginx -t

# link the two files (shouldnt be needed)
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled

# check proxy parameters (likely no issue)
sudo nano /etc/nginx/proxy_params 

```

Gunicorn
```
# Check if service is still running
sudo systemctl status main

# To edit service settings:
sudo systemctl stop main 
sudo nano /etc/systemd/system/main.service
sudo systemctl daemon-reload
sudo systemctl start main
sudo systemctl enable main

# Activate virtual environment and run gunicorn to see if it throws erros:
cd ~/face_rec/flask/ && source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 wsgi
```

Flask 
```
# Activate virtual enviroment and run scripts to see where they get stuck
cd ~/face_rec/flask/ && source venv/bin/activate
python3 main.py
```


### Creating the VM

To do: copy current VM and set up a load balancer in front of the two VM's.
https://cloud.google.com/community/tutorials/https-load-balancing-nginx

To do: write shell scripts that automatically kick off deployment of "just-as-new" VM.

requirements.txt
```
click==6.7
cmake==3.12.0
dlib==19.15.0
dominate==2.3.4
face-recognition==1.2.3
face-recognition-models==0.3.0
Flask==1.0.2
Flask-Bootstrap==3.3.7.1
gunicorn==19.9.0
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
numpy==1.15.1
Pillow==5.2.0
uWSGI==2.0.17.1
visitor==0.1.3
Werkzeug==0.14.1
```


## Appendix I: General explanation of web framework  
1. Web Frameworks & Flask  
2. Serving Flask applications
   1. WSGI server
   2. Web server
   3. Templating engine

#### Web Frameworks & Flask
Broadly speaking, a web framework consists of a set of libraries and a main handler within which you can build custom code to implement a web application (i.e. an interactive web site). Most web frameworks include patterns and utilities to accomplish at least the following:

* **URL Routing**  
Matches an incoming HTTP request to a particular piece of Python code to be invoked.

* **Request and Response Objects**   
Encapsulate the information received from or sent to a user’s browser.

* **Template Engine**  
Allows for separating Python code implementing an application’s logic from the HTML (or other) output that it produces.

* **Development Web Server**  
Runs an HTTP server on development machines to enable rapid development; often automatically reloads server-side code when files are updated

Flask is a “microframework” for Python, and is an excellent choice for building smaller applications, APIs, and web services.
Building an app with Flask is a lot like writing standard Python modules, except some functions have routes attached to them.

#### Serving Flask applications to the public  
The majority of Python applications today are hosted with a WSGI server such as Gunicorn, either directly or behind a lightweight web server such as nginx. The WSGI servers serve the applications while the web server handles tasks better suited for it such as static file serving, request routing, DDoS protection, and basic authentication.

#### 1.  WSGI server
The Web Server Gateway Interface (or “WSGI” for short) is a standard interface between web servers and Python web application frameworks. Stand-alone WSGI servers typically use less resources than traditional web servers and provide top performance.

* Gunicorn (Green Unicorn) is a pure-python WSGI server used to serve Python applications. Unlike other Python web servers, it has a thoughtful user-interface, and is extremely easy to use and configure. Gunicorn has sane and reasonable defaults for configurations. However, some other servers, like uWSGI, are tremendously more customizable, and therefore, are much more difficult to effectively use. Gunicorn is the recommended choice for new Python web applications today.

* uWSGI is a full stack for building hosting services. In addition to process management, process monitoring, and other functionality, uWSGI acts as an application server for various programming languages and protocols - including Python and WSGI. uWSGI can either be run as a stand-alone web router, or be run behind a full web server (such as Nginx or Apache). In the latter case, a web server can configure uWSGI and an application’s operation over the uwsgi protocol. uWSGI’s web server support allows for dynamically configuring Python, passing environment variables and further tuning.

#### 2. Web Server - Nginx
Nginx (pronounced “engine-x”) is a web server and reverse-proxy for HTTP, SMTP and other protocols. It is known for its high performance, relative simplicity, and compatibility with many application servers (like WSGI servers). It also includes handy features like load-balancing, basic authentication, streaming, and others. Designed to serve high-load websites, Nginx is gradually becoming quite popular.

#### 3. Templating - Jinja2
Most WSGI applications are responding to HTTP requests to serve content in HTML or other markup languages. Instead of generating directly textual content from Python, the concept of separation of concerns advises us to use templates. Jinja2 is text-based template language and can thus be used to generate any type markup, not just HTML. It allows customization of filters, tags, tests and globals.

A template engine manages a suite of template files, with a system of hierarchy and inclusion to avoid unnecessary repetition, and is in charge of rendering (generating) the actual content, filling the static content of the templates with the dynamic content generated by the application.

As template files are sometimes written by designers or front-end developers, it can be difficult to handle increasing complexity.
Some general good practices apply to the part of the application passing dynamic content to the template engine, and to the templates themselves.
*  Template files should be passed only the dynamic content that is needed for rendering the template. Avoid the temptation to pass additional content “just in case”: it is easier to add some missing variable when needed than to remove a likely unused variable later.
*  Many template engines allow for complex statements or assignments in the template itself, and many allow some Python code to be evaluated in the templates. This convenience can lead to uncontrolled increase in complexity, and often make it harder to find bugs.


## Appendix II: Side notes

Creating cookiecutter templates:
```
pip3 install cookiecutter
mkdir HelloCookieCutter1
cd HelloCookieCutter1
mkdir {{cookiecutter.directory_name}}
cd {{cookiecutter.directory_name}}
cat > {{cookiecutter.file_name}}.py << EOF
print("Hello, {{cookiecutter.greeting_recipient}}!")
EOF
```
```
cd ..
cat > cookiecutter.json << EOF
{
    "directory_name": "Hello",
    "file_name": "Howdy",
    "greeting_recipient": "Julie"
}
EOF
```