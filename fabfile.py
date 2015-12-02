from fabric.api import *

env.user = 'vagrant'
env.hosts = ['192.168.33.11']

def ruby():
    sudo('yum install -y ruby')

def git():
    sudo('yum install -y git')

def deploy():
    ruby()
    git()
