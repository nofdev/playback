# The MIT License (MIT)
#
# Copyright (c) 2015 Taio Jia (jiasir) <jiasir@icloud.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = 'jiasir'
__version__ = '0.1.0'

from fabric.api import *
from playback.config import Config


class Haproxy(Config):
    env.hosts = []

    def __init__(self):
        super(Config, self).__init__()
        config = Config()
        self.conf = config.load_conf()

        for i in range(1, 3):
            env.hosts.append(self.conf['haproxy0' + str(i) + '_host'])

    @staticmethod
    def deploy():
        sudo('apt-get update')
        sudo('apt-get install keepalived haproxy mysql-client')
        put(local_path='templates/haproxy/sysctl.conf.j2', remote_path='/etc/sysctl.conf', use_sudo=True)
        sudo('sysctl -p')

