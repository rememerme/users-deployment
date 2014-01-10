from fabric.api import env, cd, sudo, prefix
from fabric.contrib.files import exists

VIRTUALENV = '/virtualenv'
ENV = '/env'

REPO = 'users'
VIRTUALENV_NAME = 'users-api-env'

GIT_MODEL_URL = 'https://github.com/rememerme/users-model.git'
GIT_API_URL = 'https://github.com/rememerme/users-api.git'

class InstallException(Exception):
    pass

env.hosts = []
env.path = cwd()

def install():
    get_source()
    install_deps()
    setup_apache()


def get_source():
    # set up directory for env on fresh server
    if not exists(ENV, use_sudo=True):
        sudo('mkdir ' + ENV)
    with cd(ENV):
        if exists(REPO):
            raise InstallException('Repo already exists called "users" in /env/')

        sudo('mkdir ' + REPO)
        with cd(REPO):
            sudo('git pull ' + GIT_API_URL)
            sudo('git pull ' + GIT_MODEL_URL)

def install_deps(): 
    # set up directory for virtualenv
    if not exists(VIRTUALENV, use_sudo=True):
        sudo('mkdir ' + VIRTUALENV)

    sudo('virtualenv ' + VIRTUALENV_NAME)
    with cd(VIRTUALENV):
        with prefix('source ' + VIRTUALENV_NAME + '/bin/activate'):
             run('pip install -r ' + env.path +  'deps.cfg')

