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

def kill_process_at_host(
    hostname,
    pattern
):
    """Kill the process matching pattern at ip
    :param hostname: The hostname or ip address of the host on which the process will be killed
    :param pattern: A regular expression matching the name of the process to
    kill (ALL processes matching this expression will be killed)
    """
    print("Killing processes that match pattern: {} on ip: {}".format(pattern,
                                                                      ip))
    result = cmd.run_agent_cmd(ip,
                                "proc_id=$(ps ax | grep '" + pattern + "' | awk '{{ print $1 }}') && echo $proc_id")
    pids = str(result).split()
    print("Pattern: {} matched following pids: {}".format(pattern, pids))
    for pid in pids:
        result = cmd.run_agent_cmd(ip, "sudo kill -9 {}".format(pid))
        print("Killed pid: {} exit code: {}".format(pid, result.exit_code))

def shakedown_dcos_dir():
    """Gets the path to the shakedown dcos directory"""
    return os.path.dirname(os.path.realpath(__file__))
