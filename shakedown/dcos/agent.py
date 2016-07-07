"""Utilities for working with agents"""
import os

from shakedown import *

def partition_agent(
    hostname
):
    """ Partition a node from all network traffic except for SSH and loopback

        :param hostname: host or IP of the machine to partition from the cluster
    """

    copy_file_to_agent(hostname, "{}/partition_cmd".format(shakedown_dcos_dir()))
    run_command_on_agent(hostname, "sh partition_cmd")

def reconnect_agent(
    hostname
):
    """ Reconnect a previously partitioned node to the network

        :param hostname: host or IP of the machine to partition from the cluster
    """

    copy_file_to_agent(hostname, "{}/reconnect_cmd".format(shakedown_dcos_dir()))
    run_command_on_agent(hostname, "sh reconnect_cmd")

def shakedown_dcos_dir():
    """Gets the path to the shakedown dcos directory"""
    return os.path.dirname(os.path.realpath(__file__))
