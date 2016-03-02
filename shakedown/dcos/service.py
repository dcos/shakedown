from dcos import (marathon, mesos, package, util)
from dcos.errors import DCOSException


def get_service(service_name, inactive=False, completed=False):
    services = mesos.get_master().frameworks(inactive=inactive, completed=completed)

    for service in services:
        if service['name'] == service_name:
            return service

    return False


def get_service_framework_id(service_name, inactive=False, completed=False):
    service = get_service(service_name, inactive, completed)

    if service and service['id']:
        return service['id']

    return False


def get_service_tasks(service_name, inactive=False, completed=False):
    service = get_service(service_name, inactive, completed)

    if service and service['tasks']:
        return service['tasks']

    return False
