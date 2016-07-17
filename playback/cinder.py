from fabric.api import *
from fabric.contrib import files
from fabric.network import disconnect_all
from fabric.colors import red
import os
import sys
import argparse
from playback.cli import cli_description
from playback import __version__
from playback.templates.cinder_conf import conf_cinder_conf
from playback.templates.policy_json_for_cinder import conf_policy_json
from playback import common

class Cinder(common.Common):

    @runs_once
    def _create_cinder_db(self, root_db_pass, cinder_db_pass):
        print red(env.host_string + ' | Create cinder database')
        sudo("mysql -uroot -p{0} -e \"CREATE DATABASE cinder;\"".format(root_db_pass), shell=False)
        sudo("mysql -uroot -p{0} -e \"GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' IDENTIFIED BY '{1}';\"".format(root_db_pass, cinder_db_pass), shell=False)
        sudo("mysql -uroot -p{0} -e \"GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY '{1}';\"".format(root_db_pass, cinder_db_pass), shell=False)

    def create_cinder_db(self, *args, **kwargs):
        return execute(self._create_cinder_db, *args, **kwargs)

    @runs_once
    def _create_service_credentials(self, os_password, os_auth_url, cinder_pass, public_endpoint_v1, internal_endpoint_v1, admin_endpoint_v1, public_endpoint_v2, internal_endpoint_v2, admin_endpoint_v2):
        with shell_env(OS_PROJECT_DOMAIN_NAME='default',
                       OS_USER_DOMAIN_NAME='default',
                       OS_PROJECT_NAME='admin',
                       OS_TENANT_NAME='admin',
                       OS_USERNAME='admin',
                       OS_PASSWORD=os_password,
                       OS_AUTH_URL=os_auth_url, 
                       OS_IDENTITY_API_VERSION='3',
                       OS_IMAGE_API_VERSION='2'):
            print red(env.host_string + ' | Create the cinder user')
            sudo('openstack user create --domain default --password {0} cinder'.format(cinder_pass))
            print red(env.host_string + ' | Add the admin role to the cinder user and service project')
            sudo('openstack role add --project service --user cinder admin')
            print red(env.host_string + ' | Create the cinder and cinderv2 service entity')
            sudo('openstack service create --name cinder --description "OpenStack Block Storage" volume')
            sudo('openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2')
            print red(env.host_string + ' | Create the Block Storage service API endpoints')
            sudo('openstack endpoint create --region RegionOne volume public {0}'.format(public_endpoint_v1))
            sudo('openstack endpoint create --region RegionOne volume internal {0}'.format(internal_endpoint_v1))
            sudo('openstack endpoint create --region RegionOne volume admin {0}'.format(admin_endpoint_v1))
            sudo('openstack endpoint create --region RegionOne volumev2 public {0}'.format(public_endpoint_v2))
            sudo('openstack endpoint create --region RegionOne volumev2 internal {0}'.format(internal_endpoint_v2))
            sudo('openstack endpoint create --region RegionOne volumev2 admin {0}'.format(admin_endpoint_v2))

    def create_service_credentials(self, *args, **kwargs):
        return execute(self._create_service_credentials, *args, **kwargs)

    def _install(self, connection, rabbit_hosts, rabbit_user, rabbit_pass, auth_uri, auth_url, cinder_pass, my_ip, glance_api_servers, rbd_secret_uuid, memcached_servers, populate=False):
        print red(env.host_string + ' | Install the cinder-api and cinder-volume')
        sudo('apt-get update')
        sudo('apt-get -y install cinder-api cinder-scheduler cinder-volume')

        print red(env.host_string + ' | Update /etc/cinder/cinder.conf')
        with open('tmp_cinder_conf_' + env.host_string, 'w') as f:
            f.write(conf_cinder_conf)
        files.upload_template(filename='tmp_cinder_conf_' + env.host_string,
                              destination='/etc/cinder/cinder.conf',
                              use_jinja=True,
                              use_sudo=True,
                              backup=True,
                              context={'connection': connection,
                                       'rabbit_hosts': rabbit_hosts,
                                       'rabbit_user': rabbit_user,
                                       'rabbit_password': rabbit_pass,
                                       'auth_uri': auth_uri,
                                       'auth_url': auth_url,
                                       'cinder_pass': cinder_pass,
                                       'my_ip': my_ip,
                                       'glance_api_servers': glance_api_servers,
                                       'rbd_secret_uuid': rbd_secret_uuid,
                                       'memcached_servers': memcached_servers})
        os.remove('tmp_cinder_conf_' + env.host_string)

        print red(env.host_string + ' | Enable Consistency groups')
        with open('tmp_policy_json_' + env.host_string, 'w') as f:
            f.write(conf_policy_json)
        files.upload_template(filename='tmp_policy_json_' + env.host_string,
                                destination='/etc/cinder/policy.json',
                                use_sudo=True,
                                backup=True)
        os.remove('tmp_policy_json_' + env.host_string)

        if populate:
            print red(env.host_string + ' | Populate the Block Storage database')
            sudo('su -s /bin/sh -c "cinder-manage db sync" cinder', shell=False)

        print red(env.host_string + ' | Restart the services')
        sudo('service nova-api restart', warn_only=True)
        sudo('service cinder-scheduler restart')
        sudo('service cinder-api restart')
        sudo('service tgt restart', warn_only=True)
        sudo('service cinder-volume restart')
        print red(env.host_string + ' | Remove the SQLite database file')
        sudo('rm -f /var/lib/cinder/cinder.sqlite')

    def install(self, *args, **kwargs):
        return execute(self._install, *args, **kwargs)

