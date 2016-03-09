from shakedown.dcos import package as pkg
from shakedown.dcos import service as svc


def test_get_service_framework_id():
    assert svc.get_service_framework_id('spark') == None

    pkg.install_package_and_wait('spark')
    framework_id = svc.get_service_framework_id('spark')
    print('framework_id: ' + framework_id)
    assert framework_id != None

    pkg.uninstall_package_and_wait('spark')
    assert svc.get_service_framework_id('spark') == None


def test_get_service_tasks():
    pkg.install_package_and_wait('hdfs')
    service_tasks = svc.get_service_tasks('marathon')
    assert service_tasks != None

    pkg.uninstall_package_and_wait('hdfs')


def test_get_service_ips():
    pkg.install_package_and_wait('chronos')

    # Get all IPs associated with the 'chronos' task running in the 'marathon' service
    service_ips = svc.get_service_ips('marathon', 'chronos')
    print('service_ips: ' + str(service_ips))

    pkg.uninstall_package_and_wait('chronos')
