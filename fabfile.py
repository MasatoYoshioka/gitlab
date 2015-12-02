from fabric.api import *
from fabric.utils import *

env.user = 'vagrant'
env.hosts = ['192.168.33.11']

def gitlab():
    #ex)https://about.gitlab.com/downloads/#centos6
    #first step
    sudo('yum install -y curl openssh-server postfix cronie')
    sudo('service postfix start')
    sudo('chkconfig postfix on')
    sudo('lokkit -s http -s ssh')

    #second step
    run('curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh | sudo bash')
    sudo('yum install gitlab-ce')

    #last step
    sudo('gitlab-ctl reconfigure')

def ruby():
    sudo('yum install -y ruby')

def git():
    sudo('yum install -y git')

def deploy():
    ruby()
    git()
    gitlab()

def postfix():
    sudo('yum -y install cyrus-sasl-plain cyrus-sasl-md5')
    result = sudo('ls /etc/postfix/main.cf.org')
    if result.return_code != 0:
        sudo('mv /etc/postfix/main.cf /etc/postfix/main.cf.org')
    put('./postfix/main.cf', '/etc/postfix/', use_sudo=True)
    sudo('chown root:root /etc/postfix/main.cf')
    #sasl_passwd
    put('./postfix/sasl_passwd', '/etc/postfix/', use_sudo=True)
    sudo('chown root:root /etc/postfix/sasl_passwd')
    sudo('postmap /etc/postfix/sasl_passwd')
    #tls_policy
    put('./postfix/tls_policy', '/etc/postfix/', use_sudo=True)
    sudo('chown root:root /etc/postfix/tls_policy')
    sudo('postmap /etc/postfix/tls_policy')
    sudo('service postfix reload')
