######################################
### CONFIGURE DEV COMPUTE INSTANCE ###
######################################

SSH into it  
sudo -i passwd  
su   
sudo mauricerichard91  
sudo apt-get update  
sudo apt-get install tmux  
sudo apt-get install telnet  
sudo apt-get remove docker docker-engine docker.io  
sudo nano /etc/apt/sources.list  
Change deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable  
to deb [arch=amd64] https://download.docker.com/linux/ubuntu artful stable  
 
sudo apt install docker-ce  
sudo apt-get install unzip  
wget https://github.com/tiangolo/uwsgi-nginx-flask-docker/releases/download/v0.3.9/example-flask-python3.7.zip  
unzip example-flask-python3.7.zip  
cd example-flask-python3.7  
  
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
  
  
######################################  
######### DOCKER CHEATSHEET ##########  
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
  

