from dcos import (marathon, mesos, http)
from shakedown.dcos.command import *
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
    """ Get a list of tasks associated with a service
        :param service_name: the service name
        :type service_name: str
        :param inactive: whether to include inactive services
        :type inactive: bool
        :param completed: whether to include completed services
        :type completed: bool

        :return: a list of task objects
        :rtye: [dict], or None
    """

    service = get_service(service_name, inactive, completed)

    if service is not None and service['tasks']:
        return service['tasks']

    return []


def get_service_task_ids(
        service_name,
        task_predicate=None,
        inactive=False,
        completed=False
):
    """ Get a list of task IDs associated with a service
        :param service_name: the service name
        :type service_name: str
        :param task_predicate: filter function which accepts a task object and returns a boolean
        :type task_predicate: function, or None
        :param inactive: whether to include inactive services
        :type inactive: bool
        :param completed: whether to include completed services
        :type completed: bool

        :return: a list of task ids
        :rtye: [str], or None
    """
    tasks = get_service_tasks(service_name, inactive, completed)
    if task_predicate:
        return [t['id'] for t in tasks if task_predicate(t)]
    else:
        return [t['id'] for t in tasks]


def get_marathon_tasks(
        inactive=False,
        completed=False
):
    """ Get a list of marathon tasks
    """

    return get_service_tasks('marathon', inactive, completed)


def get_mesos_tasks():
    """ Get a list of mesos tasks
    """
    return mesos.get_master().tasks()


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


def get_mesos_task(task_name):
    """ Get a mesos task with a specific task name
    """
    tasks = get_mesos_tasks()

    if tasks is not None:
        for task in tasks:
            if task['name'] == task_name:
                return task
    return None


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
        :rtype: [str]
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


def mesos_task_present_predicate(task_name):
    return get_mesos_task(task_name) is not None


def mesos_task_not_present_predicate(task_name):
    return get_mesos_task(task_name) is None


def wait_for_mesos_task(task_name, timeout_sec=120):
    return time_wait(lambda: mesos_task_present_predicate(task_name), timeout_seconds=timeout_sec)


def wait_for_mesos_task_removal(task_name, timeout_sec=120):
    return time_wait(lambda: mesos_task_not_present_predicate(task_name), timeout_seconds=timeout_sec)


def delete_persistent_data(role, principal, zk_node):
    """ Deletes any persistent data associated with the specified role, principal, and zk node.

        :param role: the mesos role to delete, or None to omit this
        :type role: str
        :param principal: the mesos principal for the data to delete, or None to omit this
        :type principal: str
        :param zk_node: the zookeeper node to be deleted, or None to skip this deletion
        :type zk_node: str
    """
    janitor_cmd = ['docker run mesosphere/janitor /janitor.py']
    if role:
        janitor_cmd.append('-r {}'.format(role))
    if principal:
        janitor_cmd.append('-p {}'.format(principal))
    if zk_node:
        janitor_cmd.append('-z {}'.format(zk_node))
    janitor_cmd.append('--auth_token={}'.format(
        run_dcos_command('config show core.dcos_acs_token', print_output=False)[0].strip()))
    run_command_on_master(' '.join(janitor_cmd))


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

    return time_wait(lambda: service_unavailable_predicate(service_name), timeout_seconds=timeout_sec)


def task_states_predicate(service_name, expected_task_count, expected_task_states):
    """ Returns whether the provided service_names's tasks have expected_task_count tasks
        in any of expected_task_states. For example, if service 'foo' has 5 tasks which are
        TASK_STAGING or TASK_RUNNING.

        :param service_name: the service name
        :type service_name: str
        :param expected_task_count: the number of tasks which should have an expected state
        :type expected_task_count: int
        :param expected_task_states: the list states to search for among the service's tasks
        :type expected_task_states: [str]

        :return: True if expected_task_count tasks have any of expected_task_states, False otherwise
        :rtype: bool
    """
    try:
        tasks = get_service_tasks(service_name)
    except DCOSHTTPException:
        tasks = []
    matching_tasks = []
    other_tasks = []
    for t in tasks:
        name = t.get('name', 'UNKNOWN_NAME')
        state = t.get('state', None)
        if state and state in expected_task_states:
            matching_tasks.append(name)
        else:
            other_tasks.append('{}={}'.format(name, state))
    print('expected {} tasks in {}:\n- {} in expected {}: {}\n- {} in other states: {}'.format(
        expected_task_count, ', '.join(expected_task_states),
        len(matching_tasks), ', '.join(expected_task_states), ', '.join(matching_tasks),
        len(other_tasks), ', '.join(other_tasks)))
    return len(matching_tasks) >= expected_task_count


def wait_for_service_tasks_state(
        service_name,
        expected_task_count,
        expected_task_states,
        timeout_sec=120
):
    """ Returns once the service has at least N tasks in one of the specified state(s)

        :param service_name: the service name
        :type service_name: str
        :param expected_task_count: the expected number of tasks in the specified state(s)
        :type expected_task_count: int
        :param expected_task_states: the expected state(s) for tasks to be in, e.g. 'TASK_RUNNING'
        :type expected_task_states: [str]
        :param timeout_sec: duration to wait
        :type timeout_sec: int

        :return: the duration waited in seconds
        :rtype: int
    """
    return time_wait(
        lambda: task_states_predicate(service_name, expected_task_count, expected_task_states),
        timeout_seconds=timeout_sec)


def wait_for_service_tasks_running(
        service_name,
        expected_task_count,
        timeout_sec=120
):
    """ Returns once the service has at least N running tasks

        :param service_name: the service name
        :type service_name: str
        :param expected_task_count: the expected number of running tasks
        :type expected_task_count: int
        :param timeout_sec: duration to wait
        :type timeout_sec: int

        :return: the duration waited in seconds
        :rtype: int
    """
    return wait_for_service_tasks_state(service_name, expected_task_count, ['TASK_RUNNING'], timeout_sec)


def tasks_all_replaced_predicate(
        service_name,
        old_task_ids,
        task_predicate=None
):
    """ Returns whether ALL of old_task_ids have been replaced with new tasks

        :param service_name: the service name
        :type service_name: str
        :param old_task_ids: list of original task ids as returned by get_service_task_ids
        :type old_task_ids: [str]
        :param task_predicate: filter to use when searching for tasks
        :type task_predicate: func

        :return: True if none of old_task_ids are still present in the service
        :rtype: bool
    """
    try:
        task_ids = get_service_task_ids(service_name, task_predicate)
    except DCOSHTTPException:
        print('failed to get task ids for service {}'.format(service_name))
        task_ids = []

    print('waiting for all task ids in "{}" to change:\n- old tasks: {}\n- current tasks: {}'.format(
        service_name, old_task_ids, task_ids))
    for id in task_ids:
        if id in old_task_ids:
            return False # old task still present
    if len(task_ids) < len(old_task_ids): # new tasks haven't fully replaced old tasks
        return False
    return True


def tasks_missing_predicate(
        service_name,
        old_task_ids,
        task_predicate=None
):
    """ Returns whether any of old_task_ids are no longer present

        :param service_name: the service name
        :type service_name: str
        :param old_task_ids: list of original task ids as returned by get_service_task_ids
        :type old_task_ids: [str]
        :param task_predicate: filter to use when searching for tasks
        :type task_predicate: func

        :return: True if any of old_task_ids are no longer present in the service
        :rtype: bool
    """
    try:
        task_ids = get_service_task_ids(service_name, task_predicate)
    except DCOSHTTPException:
        print('failed to get task ids for service {}'.format(service_name))
        task_ids = []

    print('checking whether old tasks in "{}" are missing:\n- old tasks: {}\n- current tasks: {}'.format(
        service_name, old_task_ids, task_ids))
    for id in old_task_ids:
        if id not in task_ids:
            return True # an old task was not present
    return False


def wait_for_service_tasks_all_changed(
        service_name,
        old_task_ids,
        task_predicate=None,
        timeout_sec=120
):
    """ Returns once ALL of old_task_ids have been replaced with new tasks

        :param service_name: the service name
        :type service_name: str
        :param old_task_ids: list of original task ids as returned by get_service_task_ids
        :type old_task_ids: [str]
        :param task_predicate: filter to use when searching for tasks
        :type task_predicate: func
        :param timeout_sec: duration to wait
        :type timeout_sec: int

        :return: the duration waited in seconds
        :rtype: int
    """
    return time_wait(
        lambda: tasks_all_replaced_predicate(service_name, old_task_ids, task_predicate),
        timeout_seconds=timeout_sec)


def wait_for_service_tasks_all_unchanged(
        service_name,
        old_task_ids,
        task_predicate=None,
        timeout_sec=30
):
    """ Returns after verifying that NONE of old_task_ids have been removed or replaced from the service

        :param service_name: the service name
        :type service_name: str
        :param old_task_ids: list of original task ids as returned by get_service_task_ids
        :type old_task_ids: [str]
        :param task_predicate: filter to use when searching for tasks
        :type task_predicate: func
        :param timeout_sec: duration to wait until assuming tasks are unchanged
        :type timeout_sec: int

        :return: the duration waited in seconds (the timeout value)
        :rtype: int
    """
    try:
        time_wait(
            lambda: tasks_missing_predicate(service_name, old_task_ids, task_predicate),
            timeout_seconds=timeout_sec)
        # shouldn't have exited successfully: raise below
    except TimeoutExpired:
        return timeout_sec # no changes occurred within timeout, as expected
    raise DCOSException("One or more of the following tasks were no longer found: {}".format(old_task_ids))
