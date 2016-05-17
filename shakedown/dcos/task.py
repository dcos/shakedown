from dcos import mesos

from shakedown.dcos.helpers import *

import shakedown


def get_tasks(task_name='', completed=True):
    """ Get a list of tasks, optionally filtered by task name.

        :param task_name: the name of the task
        :type task_name: str
        :param completed: include completed tasks?
        :type completed: bool

        :return: a tuple of tasks
        :rtype: tuple
    """

    client = mesos.DCOSClient()
    master = mesos.Master(client.get_master_state())
    tasks = master.tasks(completed=completed, fltr=task_name)

    return tasks


def get_task(task_name='', completed=True):
    """ An alias to get_tasks()
    """

    return get_tasks(task_name=task_name, completed=completed)


def get_active_tasks(task_name=''):
    """ Get a list of active tasks, optionally filtered by task name.
    """

    return get_tasks(task_name=task_name, completed=False)


def task_completed(task_name):
    """ Check whether a task has completed.

        :param task_name: the name of the task
        :type task_name: str

        :return: True if completed, False otherwise
        :rtype: bool
    """

    tasks = get_task(task_name=task_name)

    for task in tasks:
        if task['state'] == 'TASK_FINISHED':
            return True

    return False
