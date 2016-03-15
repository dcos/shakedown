from shakedown import *


def test_install_package_and_wait():
    assert install_package_and_wait('jenkins')
    assert package_installed('jenkins')

def test_uninstall_package_and_wait():
    assert uninstall_package_and_wait('jenkins')
    assert package_installed('jenkins') == False
