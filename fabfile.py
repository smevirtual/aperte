# Copyright 2018 SME Virtual Network Contributors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Fabric file which specifies the management commands for this project.
"""
#pylint: disable=C0103

# Standard Library
import sys
import os
from contextlib import contextmanager
from functools import partial
from os.path import dirname, isdir, join

# Third Party
from fabric import api as fab
from fabric.api import local as fabric_local
from fabric.api import env

from jinja2 import Template

REPO_ROOT_DIR: str = dirname(__file__)

local_bash_command = partial(fabric_local, shell='/bin/bash')

env.virtualenv_dir: str = join(REPO_ROOT_DIR, 'venv')
env.venv_requirements_file: str = join(
    REPO_ROOT_DIR, 'requirements/venv.txt')
env.shell: str = '/bin/bash -l -i -c'
env.use_ssh_config: bool = True
env.platform: str = sys.platform.lower()

# LOCAL SETUP
# ------------------------------------------------------------------------------

def init_dev():
    """Prepare the local machine for development.
    """
    install_pip_requirements()
    ask_docker_questions()
    build_environment_files()
    install_npm_requirements()

def docker_setup(env: str):
    """TODO
    """
    pass

def ask_docker_questions():
    """TODO
    """
    pass

def install_pip_requirements(requirements_file: str = env.local_requirements_file):
    """Install pip dependencies to the local Python virtual environment within
    the repository root.

    Parameters
    ----------
    requirements_file
        Requirements file which contains pip dependencies. By default, the
        requirements file for local development environments is used if nothing
        is provided here.
    """
    verify_virtualenv()
    # Activate the virtual environment and install pip dependencies into it.
    with activate_virtualenv():
        local_bash_command('pip install -r %s' % requirements_file)

def verify_virtualenv():
    """Check if the local Python virtual environment exists within the
    repository root."""
    from distutils import spawn
    if not spawn.find_executable('virtualenv'):
        local_bash_command('sudo pip install virtualenv')

    if not isdir(env.virtualenv_dir):
        local_bash_command('virtualenv %(virtualenv_dir)s -p $(which python3)' % env)

@contextmanager
def activate_virtualenv():
    """Activate the local Python virtual environment that is in the repository
    root."""
    # pylint: disable=not-context-manager
    with fab.cd(REPO_ROOT_DIR):
        with fab.prefix('source %(virtualenv_dir)s/bin/activate' % env):
            yield

@contextmanager
def deactivate_virtualenv():
    """Deactivate the local Python virtual environment that is in the repository
    root."""
    # pylint: disable=not-context-manager
    with fab.cd(REPO_ROOT_DIR):
        with fab.prefix('source %(virtualenv_dir)s/bin/deactivate' % env):
            yield

# DEPLOY SETUP
# ------------------------------------------------------------------------------

def deploy_setup():
    """
    Prepare the repository for a GAE staging/production deployment.

    The process will ask the user questions to generate environment variable
    files and GAE deployment manifests to the repository directory.
    """
    pass

def ask_deploy_questions():
    """TODO
    """
    pass

# CLOUD SETUP
# ------------------------------------------------------------------------------

def build_environment_files():
    """
    Build and write environment variable files and cloud deployment manifests to
    the repository directory.
    """
    pass

# DJANGO MANAGEMENT
# ------------------------------------------------------------------------------

def shell():
    """Drop into an enhanced Django shell. This shell will autoload all apps
    database models for inspection and manipulation during development."""
    django_manage_command('shell_plus')

def django_manage_command(command: str):
    """Run a Django management command with 'manage.py' for administrative
    tasks.

    Parameters
    ----------
    command
        Commands and options to pass to the Django management command.
    """
    with activate_virtualenv():
        local_bash_command('python manage.py %s' % command)

# FRONTEND (JAVASCRIPT, STYLES, ASSETS)
# ------------------------------------------------------------------------------

def install_npm_requirements():
    """Install all npm requirements from the root package.json file via 'yarn'.
    """
    local_bash_command('yarn install')

# DOCKER MANAGEMENT
# ------------------------------------------------------------------------------

def docker_up(compose_file: str = 'docker.development.yaml'):
    """
    Build and run a Docker stack as specified in the provided Docker Compose
    file.

    Parameters
    ----------
    compose_file
        Docker Compile file for the Docker stack. By default, the Docker Compose
        file used is 'docker.development.yaml' in the repository root directory.
    """
    with activate_virtualenv():
        local_bash_command('docker-compose -f %s up' % compose_file)

def docker_destroy(compose_file: str = 'docker.development.yaml'):
    """
    Stops and removes all containers, networks, volumes and images created for
    the Docker stack as specified in the provided Docker Compose file.

    Parameters
    ----------
    compose_file
        Docker Compile file for the Docker stack. By default, the Docker Compose
        file used is 'docker.development.yaml' in the repository root directory.
    """
    with activate_virtualenv():
        local_bash_command("docker-compose -f %s down --rmi 'all'" % compose_file)

# LINTING AND TESTING (PYTHON)
# ------------------------------------------------------------------------------


# DEPLOYMENT
# ------------------------------------------------------------------------------

def deploy(env: str):
    """Deploy this project to Google App Engine."""
    pass
