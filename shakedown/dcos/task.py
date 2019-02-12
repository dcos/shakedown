from precisely import equal_to

from . import dcos_dns_lookup, mesos
from .service import get_service_task
from ..matcher import assert_that, eventually


def get_tasks(task_id='', completed=True):
    """ Get a list of tasks, optionally filtered by task id.
        The task_id can be the abbrevated.  Example: If a task named 'sleep' is
        scaled to 3 in marathon, there will be be 3 tasks starting with 'sleep.'

        :param task_id: task ID
        :type task_id: str
        :param completed: include completed tasks?
        :type completed: bool

        :return: a list of tasks
        :rtype: []
    """

    client = mesos.DCOSClient()
    master = mesos.Master(client.get_master_state())
    mesos_tasks = master.tasks(completed=completed, fltr=task_id)
    return [task.__dict__['_task'] for task in mesos_tasks]


def get_task(task_id, completed=True):
    """ Get a task by task id where a task_id is required.

        :param task_id: task ID
        :type task_id: str
        :param completed: include completed tasks?
        :type completed: bool

        :return: a task
        :rtype: obj
    """
    tasks = get_tasks(task_id=task_id, completed=completed)

    if len(tasks) == 0:
        return None

    assert len(tasks) == 1, 'get_task should return at max 1 task for a task id'
    return tasks[0]


def get_active_tasks(task_id=''):
    """ Get a list of active tasks, optionally filtered by task ID.
    """

    return get_tasks(task_id=task_id, completed=False)


def task_completed(task_id):
    """ Check whether a task has completed.

        :param task_id: task ID
        :type task_id: str

        :return: True if completed, False otherwise
        :rtype: bool
    """

    tasks = get_tasks(task_id=task_id)
    completed_states = ('TASK_FINISHED',
                        'TASK_FAILED',
                        'TASK_KILLED',
                        'TASK_LOST',
                        'TASK_ERROR')

    for task in tasks:
        if task['state'] in completed_states:
            return True

    return False


def wait_for_task_completion(task_id):
    """ Block until the task completes

        :param task_id: task ID
        :type task_id: str

        :rtype: None
    """
    assert_that(lambda: task_completed(task_id), eventually(equal_to(True)))


def task_property_value_predicate(service, task, prop, value):
    try:
        response = get_service_task(service, task)
    except Exception:
        pass

    return (response is not None) and (response[prop] == value)


def task_predicate(service, task):
    return task_property_value_predicate(service, task, 'state', 'TASK_RUNNING')


def task_property_present_predicate(service, task, prop):
    """ True if the json_element passed is present for the task specified.
    """
    try:
        response = get_service_task(service, task)
    except Exception:
        pass

    return (response is not None) and (prop in response)


def wait_for_task(service, task):
    """Waits for a task which was launched to be launched"""
    return assert_that(lambda: task_predicate(service, task), eventually(equal_to(True)))


def wait_for_task_property(service, task, prop):
    """Waits for a task to have the specified property"""
    assert_that(lambda: task_property_present_predicate(service, task, prop), eventually(equal_to(True)))


def wait_for_task_property_value(service, task, prop, value):
    assert_that(lambda: task_property_value_predicate(service, task, prop, value), eventually(equal_to(True)))


def dns_predicate(name):
    dns = dcos_dns_lookup(name)
    return dns[0].get('ip') is not None


def wait_for_dns(name):
    assert_that(lambda: dns_predicate(name), eventually(equal_to(True)))
