import select
import shlex
import subprocess

from shakedown.dcos.helpers import *

import shakedown


def run_command(
        host,
        command,
        username='core',
        key_path=None
):
    """ Run a command via SSH, proxied through the mesos master

        :param host: host or IP of the machine to execute the command on
        :type host: str
        :param command: the command to execute
        :type command: str
        :param username: SSH username
        :type username: str
        :param key_path: path to the SSH private key to use for SSH authentication
        :type key_path: str

        :return: True if successful, False otherwise
        :rtype: bool
    """

    if not key_path:
        key_path = shakedown.cli.ssh_key_file

    key = validate_key(key_path)

    transport = get_transport(host, username, key)
    transport = start_transport(transport, username, key)

    if transport.is_authenticated():
        print("\n{}{} $ {}\n".format(shakedown.cli.helpers.fchr('>>'), host, command))

        channel = transport.open_session()
        channel.exec_command(command)
        exit_code = channel.recv_exit_status()

        while channel.recv_ready():
            rl, wl, xl = select.select([channel], [], [], 0.0)
            if len(rl) > 0:
                recv = str(channel.recv(1024), "utf-8")
                print(recv, end='', flush=True)

        try_close(channel)
        try_close(transport)

        return exit_code == 0
    else:
        print('error: unable to authenticate ' + username + '@' + host + ' with key ' + key_path)
        return False


def run_command_on_master(
        command,
        username='core',
        key_path=None
):
    """ Run a command on the Mesos master
    """

    return run_command(shakedown.master_ip(), command, username, key_path)


def run_command_on_agent(
        host,
        command,
        username='core',
        key_path=None
):
    """ Run a command on a Mesos agent, proxied through the master
    """

    return run_command(host, command, username, key_path)


def run_dcos_command(command):
    """ Run a command via DCOS CLI

        :param command: the command to execute
        :type command: str

        :return: stdout and stderr of the command execution
        :rtype: tuple
    """

    call = shlex.split(command)
    call.insert(0, 'dcos')

    print("\n{}{}\n".format(shakedown.cli.helpers.fchr('>>'), ' '.join(call)))

    output, error = subprocess.Popen(call, stdout = subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    output = output.decode('utf-8')
    error = error.decode('utf-8')

    print(output, error)

    return output, error
