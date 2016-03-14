from shakedown.dcos import package as pkg
from shakedown.dcos import service as svc


def test_get_service_framework_id():
    assert svc.get_service_framework_id('jenkins') is None

    pkg.install_package_and_wait('jenkins')
    framework_id = svc.get_service_framework_id('jenkins')
    print('framework_id: ' + framework_id)
    assert framework_id is not None

    pkg.uninstall_package_and_wait('jenkins')
    assert svc.get_service_framework_id('jenkins') is None


def test_get_service_tasks():
    pkg.install_package_and_wait('hdfs')
    service_tasks = svc.get_service_tasks('marathon')
    assert service_tasks is not None

    pkg.uninstall_package_and_wait('hdfs')


def test_get_service_ips():
    pkg.install_package_and_wait('chronos')

    # Get all IPs associated with the 'chronos' task running in the 'marathon' service
    service_ips = svc.get_service_ips('marathon', 'chronos')
    assert service_ips is not None
    print('service_ips: ' + str(service_ips))

    pkg.uninstall_package_and_wait('chronos')
