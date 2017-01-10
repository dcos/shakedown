from dcos.mesos import DCOSClient

import shakedown


def get_resources():
    return _get_resources()


def resources_needed(total_tasks=1, per_task_cpu=0.01, per_task_mem=1):
    total_cpu = per_task_cpu * total_tasks
    total_mem = per_task_mem * total_tasks
    return Resources(total_cpu, total_mem)


def get_used_resources():
    return _get_resources('used_resources')


def get_unreserved_resources():
    return _get_resources('unreserved_resources')


def get_reserved_resources():
    return _get_resources('reserved_resources')


def available_resources():
    res = get_resources()
    used = get_used_resources()

    return res - used


def _get_resources(rtype='resources'):
    """ resource types from state summary include:  resources, used_resources
    offered_resources, reserved_resources, unreserved_resources
    The default is resources.

    :param rtype: the type of resources to return
    :type rtype: str

    :return: resources(cpu,mem)
    :rtype: Resources
    """
    cpus = 0
    mem = 0
    summary = DCOSClient().get_state_summary()

    if 'slaves' in summary:
        agents = summary.get('slaves')
        for agent in agents:
            if agent[rtype].get('cpus') is not None:
                cpus += agent[rtype].get('cpus')
            if agent[rtype].get('mem') is not None:
                mem += agent[rtype].get('mem')

    return Resources(cpus, mem)


class Resources(object):

    cpus = 0
    mem = 0

    def __init__(self, cpus=0, mem=0):
        self.cpus = cpus
        self.mem = mem

    def __str__(self):
        return "cpus: {}, mem: {}".format(self.cpus, self.mem)

    def __repr__(self):
        return "cpus: {}, mem: {}".format(self.cpus, self.mem)

    def __sub__(self, other):
        total_cpu = self.cpus - other.cpus
        total_mem = self.mem - other.mem

        return Resources(total_cpu, total_mem)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __gt__(self, other):
        return self.cpus > other.cpus and self.mem > other.cpus

    def __mul__(self, other):
        return Resources(self.cpus * other, self.mem * other)

    def __rmul__(self, other):
        return Resources(self.cpus * other, self.mem * other)

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False
