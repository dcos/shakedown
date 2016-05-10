import os
import random
import string

from shakedown import *


def test_copy_file():
    filename = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
    f = open('/tmp/' + filename, 'w')
    f.write('Hello world!')
    f.close()

    assert copy_file(master_ip(), '/tmp/' + filename)
    assert run_command(master_ip(), 'cat ' + filename)

    os.remove('/tmp/' + filename)


def test_copy_file_to_master():
    filename = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
    f = open('/tmp/' + filename, 'w')
    f.write('Hello world!')
    f.close()

    assert copy_file_to_master('/tmp/' + filename)
    assert run_command(master_ip(), 'cat ' + filename)

    os.remove('/tmp/' + filename)


def test_copy_file_to_agent():
    filename = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
    f = open('/tmp/' + filename, 'w')
    f.write('Hello world!')
    f.close()

    if not package_installed('jenkins'):
        install_package_and_wait('jenkins')

    # Get all IPs associated with the 'jenkins' task running in the 'marathon' service
    service_ips = get_service_ips('marathon', 'jenkins')
    for host in service_ips:
        assert copy_file_to_agent(host, '/tmp/' + filename)
        assert run_command_on_agent(host, 'cat ' + filename)

    if package_installed('jenkins'):
        uninstall_package_and_wait('jenkins')

    os.remove('/tmp/' + filename)


def test_copy_file_from_master():
    assert copy_file_from_master('/etc/motd')

    f = open('motd', 'r')
    print(f.read())
    f.close()


def test_copy_file_from_agent():
    if not package_installed('jenkins'):
        install_package_and_wait('jenkins')

    # Get all IPs associated with the 'jenkins' task running in the 'marathon' service
    service_ips = get_service_ips('marathon', 'jenkins')
    for host in service_ips:
        assert copy_file_from_agent(host, '/etc/motd')

    f = open('motd', 'r')
    print(f.read())
    f.close()
