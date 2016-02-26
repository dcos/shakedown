import time

import shakedown.dcos.main as dcos


def test_package_install():
    result = dcos.package_install('jenkins')
    assert result == True

def test_package_is_installed():
    result = dcos.package_installed('jenkins')
    assert result == True

def test_package_uninstall():
    result = dcos.package_uninstall('jenkins')
    assert result == True

def test_package_is_not_installed():
    result = dcos.package_installed('jenkins')
    assert result == False
