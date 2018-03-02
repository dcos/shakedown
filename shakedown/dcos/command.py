import shlex
import subprocess

from . import HostSession
from dcos.errors import DCOSException

import shakedown


def run_command(
        host,
        command,
        username=None,
        key_path=None,
        noisy=True
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
        :return: Output of command
        :rtype: string
    """
    
    with HostSession(host, username, key_path, noisy) as s:
        if noisy:
            print("\n{}{} $ {}\n".format(shakedown.fchr('>>'), host, command))
        s.exec_command(command)
    
    ec, output = s.exit_code, s.output
    return ec == 0, output


def run_command_on_master(
        command,
        username=None,
        key_path=None,
        noisy=True
):
    """ Run a command on the Mesos master
    """

    return run_command(shakedown.master_ip(), command, username, key_path, noisy)


def run_command_on_leader(
        command,
        username=None,
        key_path=None,
        noisy=True
):
    """ Run a command on the Mesos leader.  Important for Multi-Master.
    """

    return run_command(shakedown.master_leader_ip(), command, username, key_path, noisy)


def run_command_on_marathon_leader(
        command,
        username=None,
        key_path=None,
        noisy=True
):
    """ Run a command on the Marathon leader
    """

    return run_command(shakedown.marathon_leader_ip(), command, username, key_path, noisy)


def run_command_on_agent(
        host,
        command,
        username=None,
        key_path=None,
        noisy=True
):
    """ Run a command on a Mesos agent, proxied through the master
    """

    return run_command(host, command, username, key_path, noisy)


def run_dcos_command(command, raise_on_error=False, print_output=True):
    """ Run `dcos {command}` via DC/OS CLI

        :param command: the command to execute
        :type command: str
        :param raise_on_error: whether to raise a DCOSException if the return code is nonzero
        :type raise_on_error: bool
        :param print_output: whether to print the resulting stdout/stderr from running the command
        :type print_output: bool

        :return: (stdout, stderr, return_code)
        :rtype: tuple
    """

    call = shlex.split(command)
    call.insert(0, 'dcos')

    print("\n{}{}\n".format(shakedown.fchr('>>'), ' '.join(call)))

    proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()
    return_code = proc.wait()
    stdout = output.decode('utf-8')
    stderr = error.decode('utf-8')

    if print_output:
        print(stdout, stderr, return_code)

    if return_code != 0 and raise_on_error:
        raise DCOSException(
            'Got error code {} when running command "dcos {}":\nstdout: "{}"\nstderr: "{}"'.format(
            return_code, command, stdout, stderr))

    return stdout, stderr, return_code
