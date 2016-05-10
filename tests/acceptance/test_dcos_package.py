import json

from shakedown import *


def test_install_package_and_wait():
    assert install_package_and_wait('jenkins')
    assert package_installed('jenkins')

def test_uninstall_package_and_wait():
    assert uninstall_package_and_wait('jenkins')
    assert package_installed('jenkins') == False

def test_install_package_with_subcommand():
    assert install_package_and_wait('spark')
    result, error = run_dcos_command('spark --version')
    assert result.startswith('dcos-spark version')

    assert uninstall_package_and_wait('spark')
    result, error = run_dcos_command('spark --version')
    assert result.startswith("'spark' is not a dcos command.")

def test_add_package_repo():
    assert add_package_repo('Multiverse', 'https://github.com/mesosphere/multiverse/archive/version-2.x.zip', 0)

def test_get_package_repo():
    repos_json = get_package_repos()
    print(json.dumps(repos_json, sort_keys=True, indent=4, separators=(',', ': ')))
    assert repos_json['repositories'][0]['name'] == 'Multiverse'

def test_remove_package_repo():
    assert remove_package_repo('Multiverse')
