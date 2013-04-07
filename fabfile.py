from fabric.api import *
import os

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

execfile(os.path.join(PROJECT_PATH, '.deploy_settings'))

env.user = APP_USER
env.hosts = HOSTS
env.keyfile = KEY_FILE

def deploy():
    with cd(DEPLOY_PATH):
        run('git pull origin master')
        sudo('service uwsgi restart')
