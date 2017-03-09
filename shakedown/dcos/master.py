"""Utilities for working with master"""
import json

from datetime import timedelta
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


def mesos_available_predicate():
    url = master_url()
    try:
        response = http.get(url)
        return response.status_code == 200
    except Exception as e:
        return False


def wait_for_mesos_endpoint(timeout_sec=timedelta(minutes=5).total_seconds()):
    """Checks the service url if available it returns true, on expiration
    it returns false"""

    return time_wait(lambda: mesos_available_predicate(), timeout_seconds=timeout_sec)


def __mesos_zk_nodes():
    """ Returns all the children nodes under /mesos in zk
    """
    return get_zk_node_children('/mesos')


def __master_zk_nodes_keys():
    """ The masters can be registered in zk with arbitrary ids which start with
        `json.info_`.  This provides a list of all master keys.
    """
    master_zk = []
    for node in __mesos_zk_nodes():
        if 'json.info' in node['title']:
            master_zk.append(node['key'])

    return master_zk


def get_all_masters():
    """ Returns the json object that represents each of the masters.
    """
    masters = []
    for master in __master_zk_nodes_keys():
        master_zk_str = get_zk_node_data(master)['str']
        masters.append(json.loads(master_zk_str))

    return masters


def get_all_master_ips():
    """ Returns a list of IPs for the masters
    """
    ips = []
    for master in get_all_masters():
        ips.append(master['hostname'])

    return ips


@contextlib.contextmanager
def disconnected_master(incoming=True, outgoing=True):

    partition_master(incoming, outgoing)
    try:
        yield
    finally:
        # return config to previous state
        reconnect_master()
