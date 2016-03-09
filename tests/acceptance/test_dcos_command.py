from shakedown import dcos

from shakedown.dcos import command as cmd
from shakedown.dcos import package as pkg
from shakedown.dcos import service as svc


def test_run_command():
    assert cmd.run_command(dcos.master_ip(), 'cat /etc/motd') != False

def test_run_command_on_master():
    assert cmd.run_command_on_master('uname -a')

def test_run_command_on_agent():
    pkg.install_package_and_wait('jenkins')

    # Get all IPs associated with the 'jenkins' task running in the 'marathon' service
    service_ips = svc.get_service_ips('marathon', 'jenkins')
    for host in service_ips:
        assert cmd.run_command_on_agent(host, 'ps -eaf | grep -i docker | grep -i jenkins')

    pkg.uninstall_package_and_wait('jenkins')
