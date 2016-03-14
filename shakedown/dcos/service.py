from dcos import mesos


def get_service(service_name, inactive=False, completed=False):
    """ Returns a dictionary describing a service, or None """
    services = mesos.get_master().frameworks(inactive=inactive, completed=completed)

    for service in services:
        if service['name'] == service_name:
            return service

    return None


def get_service_framework_id(service_name, inactive=False, completed=False):
    """ Returns the framework ID for a service, or None """
    service = get_service(service_name, inactive, completed)

    if service is not None and service['id']:
        return service['id']

    return None


def get_service_tasks(service_name, inactive=False, completed=False):
    """ Returns all the task IDs associated with a service, or None """
    service = get_service(service_name, inactive, completed)

    if service is not None and service['tasks']:
        return service['tasks']

    return []


def get_service_ips(service_name, task_name=None, inactive=False, completed=False):
    """ Returns all the IPS associated with a service, or an empty set """
    service_tasks = get_service_tasks(service_name, inactive, completed)

    ips = set([])

    for task in service_tasks:
        if task_name is not None:
            if task['name'] == task_name:
                if task['statuses'][0]['container_status']['network_infos'][0]['ip_address']:
                    ips.add(task['statuses'][0]['container_status']['network_infos'][0]['ip_address'])
        else:
            if task['statuses'][0]['container_status']['network_infos'][0]['ip_address']:
                ips.add(task['statuses'][0]['container_status']['network_infos'][0]['ip_address'])

    return ips
