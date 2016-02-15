# Playback
Playback is an OpenStack provisioning DevOps tool that all of the OpenStack components can be deployed automation with high availability on Ubuntu based operating system.

#### Requirement
The OpenStack bare metal hosts are in MAAS environment(recommend), and all hosts are two NICs at least(external and internal).

#### Install Playback
Use pip:

    pip install playback

Or form source:

    git clone https://github.com/jiasir/playback.git
    cd playback
    git checkout liberty
    sudo python setup.py install

#### Prepare environment
Prepare the OpenStack environment.
DO NOT setup eth1 in /etc/network/interfaces

    playback-env --prepare-host --user ubuntu --hosts os02.node,os03.node,os04.node,os05.node,os06.node,os07.node,os08.node,os09.node,os10.node,os11.node,os12.node,os13.node,os14.node,os15.node,os16.node,os18.node,os19.node

Reboot the target hosts to take effect:

    playback-env --cmd "reboot" --user ubuntu --hosts os02.node,os03.node,os04.node,os05.node,os06.node,os07.node,os08.node,os09.node,os10.node,os11.node,os12.node,os13.node,os14.node,os15.node,os16.node,os18.node,os19.node

#### MySQL HA
Deploy to controller1

    playback-mysql --install --user ubuntu --hosts os02.node
    playback-mysql --config --user ubuntu --hosts os02.node --wsrep_cluster_address "gcomm://os02.node,os03.node" --wsrep_node_name="galera1" --wsrep_node_address="os02.node"

Deploy to controller2

    playback-mysql --install --user ubuntu --hosts os03.node
    playback-mysql --config --user ubuntu --hosts os03.node --wsrep_cluster_address "gcomm://os02.node,os03.node" --wsrep_node_name="galera2" --wsrep_node_address="os03.node"
