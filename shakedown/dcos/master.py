"""Utilities for working with master"""

from shakedown import *
from shakedown.cli.helpers import *

SAVE_EXISTING_RULES="if [ ! -e iptables-master.rules ] ; then sudo iptables -L > /dev/null && sudo iptables-save > iptables-master.rules ; fi;"
FLUSH_ALL_RULES="sudo iptables -F INPUT"
ALLOW_ALL="sudo iptables --policy INPUT ACCEPT && sudo iptables --policy OUTPUT ACCEPT && sudo iptables --policy FORWARD ACCEPT"
DISABLE_MASTER_INCOMING="sudo iptables -I INPUT -p tcp --dport 5050 -j REJECT"
DISABLE_MASTER_OUTGOING="sudo iptables -I OUTPUT -p tcp --sport 5050 -j REJECT"

def partition_master(incoming=True, outgoing=True):
    """ Partition master's port alone. To keep DC/OS cluster running.

    :param incoming: Partition incoming traffic to master process. Default True.
    :param outgoing: Partition outgoing traffic from master process. Default True.
    """

    echo('Partitioning master. Incoming:{} | Outgoing:{}'
        .format(incoming, outgoing))

    if incoming and outgoing:
        run_command_on_master(SAVE_EXISTING_RULES + " " + FLUSH_ALL_RULES + " && " + ALLOW_ALL + " && " + DISABLE_MASTER_INCOMING + " && " + DISABLE_MASTER_OUTGOING)
    elif incoming:
        run_command_on_master(SAVE_EXISTING_RULES + " " + FLUSH_ALL_RULES + " && " + ALLOW_ALL + " && " + DISABLE_MASTER_INCOMING)
    elif outgoing:
        run_command_on_master(SAVE_EXISTING_RULES + " " + FLUSH_ALL_RULES + " && " + ALLOW_ALL + " && " + DISABLE_MASTER_OUTGOING)
    else:
        pass


def reconnect_master():
    """ Reconnect a previously partitioned master to the network
    """

    run_command_on_master("if [ -e iptables-master.rules ]; then sudo iptables-restore < iptables-master.rules && rm iptables-master.rules ; fi")
