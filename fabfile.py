from fabric.api import *
import os

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

execfile(os.path.join(PROJECT_PATH, '.deploy_settings'))

env.user = APP_USER
env.hosts = HOSTS
env.keyfile = KEY_FILE

def deploy():
    with cd(DEPLOY_PATH):
        print '--- Pulling Changes from Server ---'
        run('git pull origin master')

        print '--- Installing Packages ---'
        sudo('pip install -r requirements.txt')

        print '--- Restarting UWSGI Instance ---'
        sudo('service uwsgi restart')
