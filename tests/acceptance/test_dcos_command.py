import json

from shakedown import *


def test_run_command():
    assert run_command(master_ip(), 'cat /etc/motd')

def test_run_command_on_master():
    assert run_command_on_master('uname -a')

def test_run_command_on_agent():
    if not package_installed('jenkins'):
        install_package_and_wait('jenkins')

    # Get all IPs associated with the 'jenkins' task running in the 'marathon' service
    service_ips = get_service_ips('marathon', 'jenkins')
    for host in service_ips:
        assert run_command_on_agent(host, 'ps -eaf | grep -i docker | grep -i jenkins')

    if package_installed('jenkins'):
        uninstall_package_and_wait('jenkins')

def test_run_dcos_command():
    result, error = run_dcos_command('package search jenkins --json')
    result_json = json.loads(result)
    assert result_json['packages'][0]['name'] == 'jenkins'
