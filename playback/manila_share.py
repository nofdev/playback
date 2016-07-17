from fabric.api import *
from fabric.contrib import files
from fabric.network import disconnect_all
from fabric.colors import red
import os
import argparse
import sys
from playback import __version__
from playback import common
from playback.templates.manila_conf_for_share import conf_manila_conf

class ManilaShare(common.Common):
    """
    Install manila share service
    
    :param user(str): the user for remote server to login 
    :param hosts(list): this is a second param
    :param key_filename(str): the ssh private key to used, default None
    :param password(str): the password for remote server
    :param parallel(bool): paralleler execute on remote server, default True
    :returns: None
    """

    def _install_manila_share(self, connection, auth_uri, auth_url, manila_pass, my_ip, memcached_servers, rabbit_hosts, rabbit_user, rabbit_pass, neutron_endpoint, neutron_pass, nova_pass, cinder_pass):
        sys.stdout.write(red(env.host_string + ' | Install manila-share python-pymysql and neutron-plugin-linuxbridge-agent\n'))
        sudo('apt update')
        sudo('apt install manila-api manila-share python-pymysql neutron-plugin-linuxbridge-agent -y')

        sys.stdout.write(red(env.host_string + ' | Update /etc/manila/manila.conf\n'))
        with open('tmp_manila_conf_' + env.host_string ,'w') as f:
            f.write(conf_manila_conf)
        files.upload_template(filename='tmp_manila_conf_' + env.host_string,
                                destination='/etc/manila/manila.conf',
                                use_jinja=True,
                                use_sudo=True,
                                backup=True,
                                context={
                                    'connection': connection,
                                    'rabbit_hosts': rabbit_hosts,
                                    'rabbit_userid': rabbit_user,
                                    'rabbit_password': rabbit_pass,
                                    'memcached_servers': memcached_servers,
                                    'auth_uri': auth_uri,
                                    'auth_url': auth_url,
                                    'manila_pass': manila_pass,
                                    'my_ip': my_ip,
                                    'neutron_endpoint': neutron_endpoint,
                                    'neutron_pass': neutron_pass,
                                    'nova_pass': nova_pass,
                                    'cinder_pass': cinder_pass
                                })
        os.remove('tmp_manila_conf_' + env.host_string)
        
        sys.stdout.write(red(env.host_string + ' | Restart the Share File Systems service including its dependencies\n'))
        finalize = sudo('systemctl restart manila-share')
        if finalize.failed or self._release == 'trusty':
            sudo('service manila-share restart')

    def install_manila_share(self, *args, **kwargs):
        return execute(self._install_manila_share, *args, **kwargs)

