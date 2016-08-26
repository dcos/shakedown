from dcos import mesos

from shakedown.dcos.helpers import *

import shakedown
import time


def get_tasks(task_id='', completed=True):
    """ Get a list of tasks, optionally filtered by task name.

        :param task_id: task ID
        :type task_id: str
        :param completed: include completed tasks?
        :type completed: bool

        :return: a tuple of tasks
        :rtype: tuple
    """

    client = mesos.DCOSClient()
    master = mesos.Master(client.get_master_state())
    tasks = master.tasks(completed=completed, fltr=task_id)

    return tasks


def get_task(task_id='', completed=True):
    """ An alias to get_tasks()
    """

    return get_tasks(task_id=task_id, completed=completed)


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

    tasks = get_task(task_id=task_id)
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
    while not task_completed(task_id):
        time.sleep(1)
