from shakedown.dcos import package as pkg
from shakedown.dcos import service as svc


def test_get_service_framework_id():
    pkg.install_package_and_wait('jenkins')
    assert svc.get_service_framework_id('jenkins') != False
    
    pkg.uninstall_package_and_wait('jenkins')
    assert svc.get_service_framework_id('jenkins') == False
