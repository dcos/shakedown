from dcos import mesos


def get_service(
        service_name,
        inactive=False,
        completed=False
):
    """ Get a dictionary describing a service
        :param service_name: the service name
        :type service_name: str
        :param inactive: whether to include inactive services
        :type inactive: bool
        :param completed: whether to include completed services
        :type completed: bool

        :return: a dict describing a service
        :rtype: dict, or None
    """

    services = mesos.get_master().frameworks(inactive=inactive, completed=completed)

    for service in services:
        if service['name'] == service_name:
            return service

    return None


def get_service_framework_id(
        service_name,
        inactive=False,
        completed=False
):
    """ Get the framework ID for a service
        :param service_name: the service name
        :type service_name: str
        :param inactive: whether to include inactive services
        :type inactive: bool
        :param completed: whether to include completed services
        :type completed: bool

        :return: a framework id
        :rtype: str, or None
    """

    service = get_service(service_name, inactive, completed)

    if service is not None and service['id']:
        return service['id']

    return None


def get_service_tasks(
        service_name,
        inactive=False,
        completed=False
):
    """ Get a list of task IDs associated with a service
        :param service_name: the service name
        :type service_name: str
        :param inactive: whether to include inactive services
        :type inactive: bool
        :param completed: whether to include completed services
        :type completed: bool

        :return: a list of services
        :rtye: list, or None
    """

    service = get_service(service_name, inactive, completed)

    if service is not None and service['tasks']:
        return service['tasks']

    return []


def get_service_ips(
        service_name,
        task_name=None,
        inactive=False,
        completed=False
):
    """ Get a set of the IPs associated with a service
        :param service_name: the service name
        :type service_name: str
        :param task_name: the task name
        :type task_name: str
        :param inactive: wehther to include inactive services
        :type inactive: bool
        :param completed: whether to include completed services
        :type completed: bool

        :return: a list of IP addresses
        :rtype: list
    """

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
