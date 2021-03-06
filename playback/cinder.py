import argparse
import os
import sys

from fabric.api import *
from fabric.colors import red
from fabric.contrib import files
from fabric.network import disconnect_all

from playback import __version__, common
from playback.templates.cinder_conf import conf_cinder_conf
from playback.templates.policy_json_for_cinder import conf_policy_json


class Cinder(common.Common):
    """
    Install cinder and volume service

    :param user(str): the user for remote server to login
    :param hosts(list): this is a second param
    :param key_filename(str): the ssh private key to used, default None
    :param password(str): the password for remote server
    :param parallel(bool): paralleler execute on remote server, default True
    :returns: None
    :examples:

        .. code-block:: python

            # create cinder instances for HA
            cinder1 = Cinder(user='ubuntu', hosts=['controller1'])
            cinder2 = Cinder(user='ubuntu', hosts=['controller2'])

            # create cinder database
            cinder1.create_cinder_db(
                root_db_pass='changeme',
                cinder_db_pass='changeme'
            )

            # create cinder service creadentials
            cinder1.create_service_credentials(
                os_password='changeme',
                os_auth_url='http://192.168.1.1:35357/v3',
                cinder_pass='changeme',
                public_endpoint_v1='http://192.168.1.1:8776/v1/%\(tenant_id\)s',
                internal_endpoint_v1='http://192.168.1.1:8776/v1/%\(tenant_id\)s',
                admin_endpoint_v1='http://192.168.1.1:8776/v1/%\(tenant_id\)s',
                public_endpoint_v2='http://192.168.1.1:8776/v2/%\(tenant_id\)s',
                internal_endpoint_v2='http://192.168.1.1:8776/v2/%\(tenant_id\)s',
                admin_endpoint_v2='http://192.168.1.1:8776/v2/%\(tenant_id\)s'
            )

            # install cinder-api and cinder-volume on controller nodes, the volume backend defaults to ceph (you must have ceph installed)
            cinder1.install(
                connection='mysql+pymysql://cinder:changeme@192.168.1.1/cinder',
                rabbit_user='openstack',
                rabbit_pass='changeme',
                rabbit_hosts='192.168.1.2,192.168.1.3',
                auth_uri='http://192.168.1.1:5000',
                auth_url='http://192.168.1.1:35357',
                cinder_pass='changeme',
                my_ip='192.168.1.2',
                glance_api_servers='http://192.168.1.1:9292',
                rbd_secret_uuid='please_use_uuidgen_to_generate',
                memcached_servers='192.168.1.2:11211,192.168.1.3:11211',
                populate=True
            )
            cinder2.install(
                connection='mysql+pymysql://cinder:changeme@192.168.1.1/cinder',
                rabbit_user='openstack',
                rabbit_pass='changeme',
                rabbit_hosts='192.168.1.2,192.168.1.3',
                auth_uri='http://192.168.1.1:5000',
                auth_url='http://192.168.1.1:35357',
                cinder_pass='changeme',
                my_ip='192.168.1.3',
                glance_api_servers='http://192.168.1.1:9292',
                rbd_secret_uuid='please_use_uuidgen_to_generate',
                memcached_servers='192.168.1.2:11211,192.168.1.3:11211',
                populate=True
            )
    """

    @runs_once
    def _create_cinder_db(self, root_db_pass, cinder_db_pass):
        print red(env.host_string + ' | Create cinder database')
        sudo(
            "mysql -uroot -p{0} -e \"CREATE DATABASE cinder;\"".format(root_db_pass), shell=False)
        sudo("mysql -uroot -p{0} -e \"GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' IDENTIFIED BY '{1}';\"".format(
            root_db_pass, cinder_db_pass), shell=False)
        sudo("mysql -uroot -p{0} -e \"GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY '{1}';\"".format(
            root_db_pass, cinder_db_pass), shell=False)

    def create_cinder_db(self, *args, **kwargs):
        """
        Create a database named `cinder` and the `cinder` user

        :param root_db_pass(str): the password of mysql `root` account
        :param cinder_db_pass(str): the password of `cinder` user:
        """
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
            sudo(
                'openstack user create --domain default --password {0} cinder'.format(cinder_pass))
            print red(env.host_string + ' | Add the admin role to the cinder user and service project')
            sudo('openstack role add --project service --user cinder admin')
            print red(env.host_string + ' | Create the cinder and cinderv2 service entity')
            sudo(
                'openstack service create --name cinder --description "OpenStack Block Storage" volume')
            sudo('openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2')
            print red(env.host_string + ' | Create the Block Storage service API endpoints')
            sudo(
                'openstack endpoint create --region RegionOne volume public {0}'.format(public_endpoint_v1))
            sudo(
                'openstack endpoint create --region RegionOne volume internal {0}'.format(internal_endpoint_v1))
            sudo(
                'openstack endpoint create --region RegionOne volume admin {0}'.format(admin_endpoint_v1))
            sudo(
                'openstack endpoint create --region RegionOne volumev2 public {0}'.format(public_endpoint_v2))
            sudo(
                'openstack endpoint create --region RegionOne volumev2 internal {0}'.format(internal_endpoint_v2))
            sudo(
                'openstack endpoint create --region RegionOne volumev2 admin {0}'.format(admin_endpoint_v2))

    def create_service_credentials(self, *args, **kwargs):
        r"""
        Create the cinder service credentials

        :param os_password(str): the password of OpenStack `admin` user
        :param os_auth_url(str): keystone endpoint url e.g. `http://CONTROLLER_VIP:35357/v3`
        :param cinder_pass(str): password of `cinder` user
        :param public_endpoint_v1(str): public endpoint for volume service e.g. `http://CONTROLLER_VIP:8776/v1/%\\(tenant_id\\)s`
        :param internal_endpoint_v1(str): internal endpoint for volume service e.g. `http://CONTROLLER_VIP:8776/v1/%\\(tenant_id\\)s`
        :param admin_endpoint_v1(str): admin endpoint for volume service e.g. `http://CONTROLLER_VIP:8776/v1/%\\(tenant_id\\)s`
        :param public_endpoint_v2(str): public endpoint v2 for volumev2 service e.g. `http://CONTROLLER_VIP:8776/v2/%\\(tenant_id\\)s`
        :param internal_endpoint_v2(str): internal endpoint v2 for volumev2 service e.g. `http://CONTROLLER_VIP:8776/v2/%\\(tenant_id\\)s`
        :param admin_endpoint_v2(str): admin endpoint v2 for volumev2 service e.g. `http://CONTROLLER_VIP:8776/v2/%\\(tenant_id\\)s`
        """
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
        """
        Install cinder and volume service

        :param connection: The SQLAlchemy connection string to use to connect to the database. (string value) e.g. `mysql+pymysql://cinder:CINDER_PASS@CONTROLLER_VIP/cinde`
        :param rabbit_hosts: RabbitMQ HA cluster host:port pairs. (list value) e.g. `CONTROLLER1,CONTROLLER2`
        :param rabbit_user(str): The RabbitMQ userid. (string value) e.g. `openstack`
        :param rabbit_pass(str): The RabbitMQ password. (string value)
        :param auth_uri(str): Complete public Identity API endpoint. (string value) e.g. `http://CONTROLLER_VIP:5000`
        :param auth_url(str): Complete admin Identity API endpoint. (string value) e.g. `http://CONTROLLER_VIP:35357`
        :param cinder_pass(str): create a password of `cinder` database user
        :param my_ip(str): IP address of this host (string value)
        :param glance_api_servers(str): A list of the URLs of glance API servers available to cinder ([http[s]://][hostname|ip]:port). If protocol is not specified it defaults to http. (list value) e.g. `http://CONTROLLER_VIP:9292`
        :param rbd_secret_uuid(str): (String) The libvirt uuid of the secret for the rbd_user volumes (string value) , use `uuidgen` to generate the ceph uuid
        :param memcached_servers(str): Optionally specify a list of memcached server(s) to use for caching. If left undefined, tokens will instead be cached in-process. (list value) e.g. `CONTROLLER1:11211,CONTROLLER2:11211`
        :param populate(bool): Populate the cinder database, default `False`
        """
        return execute(self._install, *args, **kwargs)
