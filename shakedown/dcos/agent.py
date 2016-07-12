
from shakedown import *

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
        for reservation in agent["reserved_resources"]:
            if "slave_public" not in reservation:
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
    slaves = client.get_state_summary()['slaves']
    return slaves
