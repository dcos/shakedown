"""Utilities for working with master"""

from shakedown import *


def partition_master(incoming=True, outgoing=True):
    """ Partition master's port alone. To keep DC/OS cluster running.
    """

    print('Partitioning master. Incoming:{} | Outgoing:{}'
        .format(incoming, outgoing))

    if incoming and outgoing:
        run_command_on_master("if [ ! -e iptables-master.rules ] ; then sudo iptables -L > /dev/null && sudo iptables-save > iptables-master.rules ; fi; sudo iptables -F INPUT && sudo iptables --policy INPUT ACCEPT && sudo iptables --policy OUTPUT ACCEPT && sudo iptables --policy FORWARD ACCEPT && sudo iptables -I INPUT -p tcp --dport 5050 -j REJECT && sudo iptables -I OUTPUT -p tcp --sport 5050 -j REJECT")
    elif incoming:
        run_command_on_master("if [ ! -e iptables-master.rules ] ; then sudo iptables -L > /dev/null && sudo iptables-save > iptables-master.rules ; fi; sudo iptables -F INPUT && sudo iptables --policy INPUT ACCEPT && sudo iptables --policy OUTPUT ACCEPT && sudo iptables --policy FORWARD ACCEPT && sudo iptables -I INPUT -p tcp --dport 5050 -j REJECT")
    elif outgoing:
        run_command_on_master("if [ ! -e iptables-master.rules ] ; then sudo iptables -L > /dev/null && sudo iptables-save > iptables-master.rules ; fi; sudo iptables -F INPUT && sudo iptables --policy INPUT ACCEPT && sudo iptables --policy OUTPUT ACCEPT && sudo iptables --policy FORWARD ACCEPT && sudo iptables -I OUTPUT -p tcp --sport 5050 -j REJECT")
    else:
        pass


def reconnect_master():
    """ Reconnect a previously partitioned master to the network
    """

    run_command_on_master("if [ -e iptables-master.rules ]; then sudo iptables-restore < iptables-master.rules && rm iptables-master.rules ; fi")
