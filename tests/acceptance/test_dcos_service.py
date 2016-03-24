from shakedown import *


def test_get_service_framework_id():
    assert get_service_framework_id('jenkins') is None

    install_package_and_wait('jenkins')
    framework_id = get_service_framework_id('jenkins')
    print('framework_id: ' + framework_id)
    assert framework_id is not None

    uninstall_package_and_wait('jenkins')
    assert get_service_framework_id('jenkins') is None


def test_get_service_tasks():
    install_package_and_wait('hdfs')
    service_tasks = get_service_tasks('marathon')
    assert service_tasks is not None

    uninstall_package_and_wait('hdfs')


def test_get_service_task():
    install_package_and_wait('jenkins')
    service_task = get_service_task('marathon', 'jenkins')
    assert service_task is not None

    uninstall_package_and_wait('jenkins')


def test_get_service_ips():
    install_package_and_wait('chronos')

    # Get all IPs associated with the 'chronos' task running in the 'marathon' service
    service_ips = get_service_ips('marathon', 'chronos')
    assert service_ips is not None
    print('service_ips: ' + str(service_ips))

    uninstall_package_and_wait('chronos')
