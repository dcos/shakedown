import json

from shakedown import *


def test_run_command():
    exit_status, output = run_command(master_ip(), 'cat /etc/motd')
    assert exit_status
    assert 'Core' in output

def test_run_command_on_master():
    exit_status, output = run_command_on_master('uname -a')
    assert exit_status
    assert output.startswith('Linux')

def test_run_command_on_leader():
    exit_status, output = run_command_on_leader('uname -a')
    assert exit_status
    assert output.startswith('Linux')

def test_run_command_on_marathon_leader():
    exit_status, output = run_command_on_marathon_leader('uname -a')
    assert exit_status
    assert output.startswith('Linux')

def test_run_command_on_agent():
    # Get all IPs associated with the 'jenkins' task running in the 'marathon' service
    service_ips = get_service_ips('marathon', 'jenkins')
    for host in service_ips:
        exit_status, output = run_command_on_agent(host, 'ps -eaf | grep -i docker | grep -i jenkins')
        assert exit_status
        assert output.startswith('root')

def test_run_dcos_command():
    stdout, stderr, return_code = run_dcos_command('package search jenkins --json')
    result_json = json.loads(stdout)
    assert result_json['packages'][0]['name'] == 'jenkins'
