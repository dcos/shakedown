import socket

from shakedown import *


def test_get_public_agents():
    public_agents = get_public_agents()

    assert isinstance(public_agents, list)
    print(public_agents)
    try:
        assert socket.inet_aton(public_agents[0])
    except:
        assert False


def test_get_public_agents_public_ip():
    public_ips = get_public_agents_public_ip()

    assert isinstance(public_ips, list)

    try:
        assert socket.inet_aton(public_ips[0])
    except:
        assert False


def test_get_private_agents():
    private_agents = get_private_agents()

    assert isinstance(private_agents, list)

    try:
        assert socket.inet_aton(private_agents[0])
    except:
        assert False


def test_get_agents():
    agents = get_agents()

    assert isinstance(agents, list)

    try:
        assert socket.inet_aton(agents[0])
    except:
        assert False
