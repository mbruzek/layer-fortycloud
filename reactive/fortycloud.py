import os

from shlex import split
from shutil import copy2
from subprocess import check_call

from charms.docker.compose import Compose
from charms.reactive import hook
from charms.reactive import remove_state
from charms.reactive import set_state
from charms.reactive import when
from charms.reactive import when_not

from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import is_leader
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.templating import render
from charmhelpers.core import unitdata
from charmhelpers.core.host import chdir
from contextlib import contextmanager

@when_not('fortycloud.installed')
def install():
    ''' start state'''
    # apt-get install fortycloud.
    curl http://fortycloud.com/api/install
    ./install_fortycloud
    set_state('fortycloud.installed')

@when('fortycloud.installed')
@when_not('fortycloud.configured')
def config():
    ''' intermediate state '''
    # set value in config files, run scripts.
    config = hookenv.config()
    key = config['activation-key']
    subprocess.call('./install_fortycloud {}'.format(key))
    set_state("fortycloud.configured")

@when('fortycloud.configured')
def final():
   ''' This is the final state that is always true.'''
   config = hookenv.config()
   if config.changed('activation-key'):
       remove_state('fortycloud.configured')
