from dcos import (marathon, mesos, http)
from shakedown.dcos.spinner import *
from shakedown.dcos import dcos_service_url
from dcos.errors import DCOSException, DCOSHTTPException

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


def get_marathon_tasks(
    inactive=False,
    completed=False
):
    """ Get a list of marathon tasks
    """

    return get_service_tasks('marathon', inactive, completed)


def get_service_task(
        service_name,
        task_name,
        inactive=False,
        completed=False
):
    """ Get a dictionary describing a service task, or None
        :param service_name: the service name
        :type service_name: str
        :param task_name: the task name
        :type task_name: str
        :param inactive: whether to include inactive services
        :type inactive: bool
        :param completed: whether to include completed services
        :type completed: bool

        :return: a dictionary describing the service
        :rtye: dict, or None
    """

    service = get_service_tasks(service_name, inactive, completed)

    if service is not None:
        for task in service:
            if task['name'] == task_name:
                return task

    return None


def get_marathon_task(
    task_name,
    inactive=False,
    completed=False
):
    """ Get a dictionary describing a named marathon task
    """

    return get_service_task('marathon', task_name, inactive, completed)


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
        if task_name is None or task['name'] == task_name:
            for ip in task['statuses'][0]['container_status']['network_infos'][0]['ip_addresses']:
                ips.add(ip['ip_address'])

    return ips


def service_healthy(service_name, app_id=None):
    """ Check whether a named service is healthy

        :param service_name: the service name
        :type service_name: str
        :param app_id: app_id to filter
        :type app_id: str

        :return: True if healthy, False otherwise
        :rtype: bool
    """

    marathon_client = marathon.create_client()
    apps = marathon_client.get_apps_for_framework(service_name)

    if apps:
        for app in apps:
            if (app_id is not None) and (app['id'] != "/{}".format(str(app_id))):
                continue

            if (app['tasksHealthy']) \
            and (app['tasksRunning']) \
            and (not app['tasksStaged']) \
            and (not app['tasksUnhealthy']):
                return True

    return False


def service_available_predicate(service_name):
    url = dcos_service_url(service_name)
    try:
        response = http.get(url)
        return response.status_code == 200
    except Exception as e:
        return False


def service_unavailable_predicate(service_name):
    url = dcos_service_url(service_name)
    try:
        response = http.get(url)
    except DCOSHTTPException as e:
        if e.response.status_code == 500:
            return True
    else:
        return False


def wait_for_service_endpoint(service_name, timeout_sec=120):
    """Checks the service url if available it returns true, on expiration
    it returns false"""

    return time_wait(lambda: service_available_predicate(service_name), timeout_seconds=timeout_sec)


def wait_for_service_endpoint_removal(service_name, timeout_sec=120):
    """Checks the service url if it is removed it returns true, on expiration
    it returns false"""

    return time_wait(lambda: service_unavailable_predicate(service_name))
