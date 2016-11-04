"""Utilities for working with agents"""

from shakedown import *
import os
from dcos import (marathon, mesos)


def get_public_agents():
    """Provides a list of hostnames / IPs that are public agents in the cluster"""
    agent_list = []
    agents = __get_all_agents()
    for agent in agents:
        for reservation in agent["reserved_resources"]:
            if "slave_public" in reservation:
                agent_list.append(agent["hostname"])

    return agent_list


def get_private_agents():
    """Provides a list of hostnames / IPs that are private agents in the cluster"""

    agent_list = []
    agents = __get_all_agents()
    for agent in agents:
        if(len(agent["reserved_resources"]) == 0):
            agent_list.append(agent["hostname"])
        else:
            private = True
            for reservation in agent["reserved_resources"]:
                if("slave_public" in reservation):
                    private = False

            if(private):
                agent_list.append(agent["hostname"])

    return agent_list


def get_agents():
    """Provides a list of hostnames / IPs of all agents in the cluster"""

    agent_list = []
    agents = __get_all_agents()
    for agent in agents:
        agent_list.append(agent["hostname"])

    return agent_list


def __get_all_agents():
    """Provides all agent json in the cluster which can be used for filtering"""

    client = mesos.DCOSClient()
    agents = client.get_state_summary()['slaves']
    return agents


def partition_agent(host):
    """ Partition a node from all network traffic except for SSH and loopback

        :param hostname: host or IP of the machine to partition from the cluster
    """

    save_iptables(host)
    flush_all_rules(host)
    allow_all_traffic(host)

    copy_file_to_agent(host, "{}/partition_cmd".format(shakedown_dcos_dir()))
    run_command_on_agent(host, "sh partition_cmd")


def reconnect_agent(host):
    """ Reconnect a previously partitioned node to the network

        :param hostname: host or IP of the machine to partition from the cluster
    """

    restore_iptables(host)


@contextlib.contextmanager
def disconnected_agent(host):

    partition_agent(host)
    try:
        yield
    finally:
        # return config to previous state
        reconnect_agent(host)


def kill_process_on_host(
    hostname,
    pattern
):
    """ Kill the process matching pattern at ip

        :param hostname: the hostname or ip address of the host on which the process will be killed
        :param pattern: a regular expression matching the name of the process to kill
    """

    status, stdout = run_command_on_agent(hostname, "ps aux | grep -v grep | grep '{}'".format(pattern))
    pids = [p.strip().split()[1] for p in stdout.splitlines()]

    for pid in pids:
        status, stdout = run_command_on_agent(hostname, "sudo kill -9 {}".format(pid))
        if status:
            print("Killed pid: {}".format(pid))
        else:
            print("Unable to killed pid: {}".format(pid))


def restart_agent(
    hostname
):
    """ Restarts an agent process at the host

    :param hostname: host or IP of the machine to restart the agent process.
    """

    run_command_on_agent(hostname, "sudo systemctl restart dcos-mesos-slave")


def stop_agent(
    hostname
):
    """ Stops an agent process at the host

    :param hostname: host or IP of the machine to stop the agent process.
    """

    run_command_on_agent(hostname, "sudo systemctl stop dcos-mesos-slave")


def start_agent(
    hostname
):
    """ Starts an agent process at the host

    :param hostname: host or IP of the machine to start the agent process.
    """

    run_command_on_agent(hostname, "sudo systemctl start dcos-mesos-slave")


def restart_agent_node(hostname):
    """ Restarts the agent node
    """

    run_command_on_agent(hostname, "sudo /sbin/shutdown -r now")


def delete_agent_log(
    hostname
):
    """ Deletes the agent log at the host.  This is necessary if any changes
    occurred to the agent resources and the agent is restarted.

    :param hostname: host or IP of the machine to delete the agent log.
    """

    run_command_on_agent(hostname, "sudo rm -f /var/lib/mesos/slave/meta/slaves/latest")


def shakedown_dcos_dir():
    """Gets the path to the shakedown dcos directory"""
    return os.path.dirname(os.path.realpath(__file__))
