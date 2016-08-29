"""Utilities for working with master"""

from shakedown import *


def partition_master(incoming=True, outgoing=True):
    """ Partition Master's port alone. To keep DC/OS cluster running.
    """

    print('Partitioning master. Incoming:{} | Outgoing:{}'
        .format(incoming, outgoing))

    if incoming and outgoing:
        copy_file_to_master("{}/partition_master_cmd"
            .format(shakedown_dcos_dir()))
        run_command_on_master("sh partition_master_cmd")
    elif incoming:
        copy_file_to_master("{}/partition_master_incoming_cmd"
            .format(shakedown_dcos_dir()))
        run_command_on_master("sh partition_master_incoming_cmd")
    elif outgoing:
        copy_file_to_master("{}/partition_master_outgoing_cmd"
            .format(shakedown_dcos_dir()))
        run_command_on_master("sh partition_master_outgoing_cmd")
    else:
        pass


def reconnect_master():
    """ Reconnect a previously partitioned master to the network
    """

    copy_file_to_master("{}/reconnect_master_cmd".format(shakedown_dcos_dir()))
    run_command_on_master("sh reconnect_master_cmd")
