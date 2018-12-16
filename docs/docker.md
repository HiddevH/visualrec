
 
######################################
#### BUILD DOCKERFILE AND USE IN APP ENGINE ####
######################################

Previous was on starting new VM.
Next is using the standard dockerfile from the git repo. We're going to build an image and upload it to docker hub so we can use it in the app engine

On a regular VM (preferably lots of ram/cpu)
```
git clone https://github.com/ageitgey/face_recognition.git
cd face_recognition
sudo docker build -t myimage .  
export DOCKER_ID_USER=mr1991  
sudo docker login  
sudo docker tag myimage $DOCKER_ID_USER/myimage  
sudo docker push $DOCKER_ID_USER/myimage  
```

On the app engine
```
sudo docker pull mr1991/myimage  
```


 
 
 
 
 
 
 
######################################  
#### DOCKER CHEATSHEET #####  
######################################  
  
## List Docker CLI commands  
sudo docker  
sudo docker container --help  
  
## Display Docker version and info  
sudo docker --version  
sudo docker version  
sudo docker info  
  
## Execute Docker image  
sudo docker run hello-world  
  
## List Docker images  
sudo docker image ls  
  
## List Docker containers (running, all, all in quiet mode)  
sudo docker container ls  
sudo docker container ls --all  
sudo docker container ls -aq  

#####################################  
### BUILD AND TEST CONTAINER ####  
#####################################  
  
Build image (always do this whenever you change something in Dockerfile/compose.yml)  
sudo docker build -t myimage .  

Background container:  
sudo docker run -d --name mycontainer -p 80:80 myimage  
  
Interactive container:  
sudo docker run --interactive --name mycontainer --tty -p 80:80 myimage  
  
Remove container:  
sudo docker rm -f mycontainer  
  
Show containers:  
sudo docker container ls  
  
Run below in ~/example-flask-python3.7 for background session where you can change the python script:  
sudo docker run -d --name mycontainer -p 80:80 -v $(pwd)/app:/app -e FLASK_APP=main.py -e FLASK_DEBUG=1 myimage flask run --host=0.0.0.0 --port=80  
  
  
######################################  
#### PUBLISH IMAGE TO DOCKER HUB #####  
######################################  
  
sudo docker build -t myimage .  
export DOCKER_ID_USER=mr1991  
sudo docker login  
sudo docker tag myimage $DOCKER_ID_USER/myimage  
sudo docker push $DOCKER_ID_USER/myimage  
  
  
 
 

OLD:
  
######################################
### CONFIGURE DEV COMPUTE INSTANCE ###
######################################


SSH into compute engine and execute the following
```
sudo -i passwd  
sudo apt-get update  
sudo apt-get install tmux  
sudo apt-get install telnet  
```


```
cat > ~/.bash_aliases <<EOF
alias1='sudo nano ~/.bash_aliases'
alias2='sudo source ~/.bashrc'
EOF
```
```
source ~/.bash_aliases
```
On Ubuntu  18.04, install docker:
```
sudo apt-get remove docker docker-engine docker.io  
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable"
sudo apt-get update

apt-cache search docker-ce
# should give docker-ce - Docker: the open-source application container engine

sudo apt-get install docker-ce
```
Get example flask project:
```
sudo apt-get install unzip  
wget https://github.com/tiangolo/uwsgi-nginx-flask-docker/releases/download/v0.3.9/example-flask-python3.7.zip  
unzip example-flask-python3.7.zip  
cd example-flask-python3.7  
``` 

```
sudo apt-get install virtualenv
sudo apt-get install python-pip
sudo apt-get install python3.7
virtualenv --python python3.7 venv
source venv/bin/activate
```

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

```
pip install -r requirements.txt
```

// I quit here