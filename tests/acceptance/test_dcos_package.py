from shakedown.dcos import package as pkg


def test_install_package_and_wait():
    assert pkg.install_package_and_wait('jenkins') == True
    assert pkg.package_installed('jenkins') == True

def test_uninstall_package_and_wait():
    assert pkg.uninstall_package_and_wait('jenkins') == True
    assert pkg.package_installed('jenkins') == False
