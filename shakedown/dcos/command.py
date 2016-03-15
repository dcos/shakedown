import paramiko
import select

from shakedown.cli.helpers import *
from shakedown.dcos import *


def run_command(
    host,
    command,
    username='core',
    key_path=ssh_key_path()
):
    """ Run a command via SSH, proxyied through the mesos master

        host (str): host or IP of the machine to execute the command on
        command (str): the command to execute
        username (str): SSH username
        key_path (str): path to the SSH private key to use for SSH authentication
    """
    if not os.path.isfile(key_path):
        print('error: key not found: ' + key_path)
        return False

    key = paramiko.RSAKey.from_private_key_file(key_path)

    transport = None

    if host == master_ip():
        transport = paramiko.Transport(host)
    else:
        transport_master = paramiko.Transport(master_ip())
        _start_transport(transport_master, username, key)

        if not transport_master.is_authenticated():
           print('error: unable to authentication ' + username + '@' + master_ip() + ' with key ' + key_path)
           return False

        channel = transport_master.open_channel('direct-tcpip', (host, 22), ('127.0.0.1', 0))
        transport = paramiko.Transport(channel)

    _start_transport(transport, username, key)

    if transport.is_authenticated():
        print("\n" + fchr('>>') + host + " $ " + command + "\n")

        channel = transport.open_session()
        channel.exec_command(command)
        channel.recv_exit_status()

        while channel.recv_ready():
            rl, wl, xl = select.select([channel], [], [], 0.0)
            if len(rl) > 0:
                recv = str(channel.recv(1024), "utf-8")
                print(recv, end='', flush=True)

        channel.close()
        transport.close()

        if host != master_ip():
            transport_master.close()

        return True
    else:
        print('error: unable to authentication ' + username + '@' + host + ' with key ' + key_path)
        return False


def run_command_on_master(
    command,
    username='core',
    key_path=ssh_key_path()
):
    return run_command(master_ip(), command, username, key_path)


def run_command_on_agent(
    host,
    command,
    username='core',
    key_path=ssh_key_path()
):
    return run_command(host, command, username, key_path)


def _start_transport(transport, username, key):
    transport.start_client()
    transport.auth_publickey(username, key)

    return transport
