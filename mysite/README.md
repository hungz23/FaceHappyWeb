#Step 1: Install Package
### [install python-pip](https://pip.pypa.io/en/stable/installing/)
### [install ansible](http://docs.ansible.com/ansible/latest/intro_installation.html)
### fix playbook for system and run commandline: $ansible-playbook InstallPlaybook.yaml
#Step 2: Setup Environment
### Go to this directory
### Setup Redis Server: $systemctl status redis.service
#Step 3: Run
### Go to this directory
### Add your ip to Allow_host in mysite/setting/py
### Terminal 1: $python manage.py runsslserver host:port (Ex: $python manage.py runsslserver 0.0.0.0:8000)
### Terminal 2: $export PYTHONPATH=/vagrant/django/FaceHappyWeb/mysite/facenet/src; $celery -A polls worker -l info
### Terminal 3: $celery -A polls beat -l info
