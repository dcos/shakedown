import json

from shakedown import *


def test_install_package_and_wait():
    assert not package_installed('chronos')
    install_package_and_wait('chronos')
    assert package_installed('chronos')

def test_uninstall_package_and_wait():
    assert package_installed('chronos')
    uninstall_package_and_wait('chronos')
    assert package_installed('chronos') == False

def test_install_package_with_json_options():
    install_package_and_wait('chronos', None, 'big-chronos', None, {"chronos": {"cpus": 2}})
    assert get_service_task('marathon', 'big-chronos')['resources']['cpus'] == 2
    uninstall_package_and_wait('chronos')

def test_install_package_with_subcommand():
    install_package_and_wait('riak')
    result, err = run_dcos_command('riak --version')
    assert result.startswith('0')

def test_uninstall_package_with_subcommand():
    uninstall_package_and_wait('riak')
    result, err = run_dcos_command('riak --version')
    assert err.endswith("is not a dcos command.\n")

def test_add_package_repo():
    assert add_package_repo('Multiverse', 'https://github.com/mesosphere/multiverse/archive/version-2.x.zip', 0)

def test_get_package_repo():
    repos_json = get_package_repos()
    print(json.dumps(repos_json, sort_keys=True, indent=4, separators=(',', ': ')))
    assert repos_json['repositories'][0]['name'] == 'Multiverse'

def test_remove_package_repo():
    assert remove_package_repo('Multiverse')
