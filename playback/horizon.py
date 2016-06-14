from fabric.api import *
from fabric.contrib import files
from fabric.tasks import Task
from fabric.network import disconnect_all
from fabric.colors import red
import os
import argparse
import sys
from playback.cli import cli_description
from playback import __version__
from playback.horizon_conf import conf_local_settings_py

class Horizon(Task):
    def __init__(self, user, hosts=None, parallel=True, *args, **kwargs):
        super(Horizon, self).__init__(*args, **kwargs)
        self.user = user
        self.hosts = hosts
        self.parallel = parallel
        env.user = self.user
        env.hosts = self.hosts
        env.parallel = self.parallel

    @runs_once
    def _install(self, openstack_host, memcache, time_zone):
        print red(env.host_string + ' | Install the packages')
        sudo('apt-get update')
        sudo('apt-get -y install openstack-dashboard')

        print red(env.host_string + ' | Update /etc/openstack-dashboard/local_settings.py')
        with open('tmp_local_settings_py_' + env.host_string, 'w') as f:
            f.write(conf_local_settings_py)
        files.upload_template(filename='tmp_local_settings_py_' + env.host_string,
                              destination='/etc/openstack-dashboard/local_settings.py',
                              use_jinja=True,
                              use_sudo=True,
                              context={'openstack_host': openstack_host,
                                       'memcache': memcache,
                                       'time_zone': time_zone})
        os.remove('tmp_local_settings_py_' + env.host_string)

def install(args):
    try:
        target = Horizon(user=args.user, hosts=args.hosts.split(','))
    except AttributeError:
        sys.stderr.write(red('No hosts found. Please using --hosts param.'))
        sys.exit(1)

    execute(target._install, 
            args.openstack_host, 
            args.memcache, 
            args.time_zone)

def parser():
    p = argparse.ArgumentParser(prog='playback-horizon', description=cli_description+'this command used for provision Horizon')
    p.add_argument('-v', '--version',
                    action='version',
                    version=__version__)
    p.add_argument('--user', 
                    help='the target user', 
                    action='store', 
                    default='ubuntu', 
                    dest='user')
    p.add_argument('--hosts', 
                    help='the target address', 
                    action='store', 
                    dest='hosts')
    s = p.add_subparsers(dest='subparser_name')

    def install_f(args):
        install(args)
    install_parser = s.add_parser('install', help='install horizon')
    install_parser.add_argument('--openstack-host',
                                help='configure the dashboard to use OpenStack services on the controller node e.g. CONTROLLER_VIP',
                                action='store',
                                default=None,
                                dest='openstack_host')
    install_parser.add_argument('--memcache',
                                help='django memcache e.g. CONTROLLER1:11211',
                                action='store',
                                default=None,
                                dest='memcache')
    install_parser.add_argument('--time-zone',
                                help='the timezone of the server. This should correspond with the timezone of your entire OpenStack installation e.g. Asia/Shanghai',
                                action='store',
                                default=None,
                                dest='time_zone')
    install_parser.set_defaults(func=install_f)

    return p

def main():
    p = parser()
    args = p.parse_args()
    if not hasattr(args, 'func'):
        p.print_help()
    else:
        # XXX on Python 3.3 we get 'args has no func' rather than short help.
        try:
            args.func(args)
            disconnect_all()
            return 0
        except Exception as e:
            sys.stderr.write(e.message)
            sys.exit(1)
    return 1

if __name__ == '__main__':
    main()