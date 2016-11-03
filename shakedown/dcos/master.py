"""Utilities for working with master"""

from shakedown import *
from shakedown.cli.helpers import *

DISABLE_MASTER_INCOMING="sudo iptables -I INPUT -p tcp --dport 5050 -j REJECT"
DISABLE_MASTER_OUTGOING="sudo iptables -I OUTPUT -p tcp --sport 5050 -j REJECT"


def partition_master(incoming=True, outgoing=True):
    """ Partition master's port alone. To keep DC/OS cluster running.

    :param incoming: Partition incoming traffic to master process. Default True.
    :param outgoing: Partition outgoing traffic from master process. Default True.
    """

    echo('Partitioning master. Incoming:{} | Outgoing:{}'.format(incoming, outgoing))

    save_iptables(shakedown.master_ip())
    flush_all_rules(shakedown.master_ip())
    allow_all_traffic(shakedown.master_ip())

    if incoming and outgoing:
        run_command_on_master(DISABLE_MASTER_INCOMING + " && " + DISABLE_MASTER_OUTGOING)
    elif incoming:
        run_command_on_master(DISABLE_MASTER_INCOMING)
    elif outgoing:
        run_command_on_master(DISABLE_MASTER_OUTGOING)
    else:
        pass


def reconnect_master():
    """ Reconnect a previously partitioned master to the network
    """

    reconnect_node(shakedown.master_ip())


def restart_master_node():
    """ Restarts the master node
    """

    run_command_on_master("sudo /sbin/shutdown -r now")


def systemctl_master(command='restart'):
    """ Used to start, stop or restart the master process
    """
    run_command_on_master('sudo systemctl {} dcos-mesos-master'.format(command))


@contextlib.contextmanager
def disconnected_master(incoming=True, outgoing=True):

    partition_master(incoming, outgoing)
    try:
        yield
    finally:
        # return config to previous state
        reconnect_master()
