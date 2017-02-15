from dcos.mesos import DCOSClient
from distutils.version import LooseVersion

import pytest
import shakedown


dcos_1_10 = pytest.mark.skipif('dcos_version_less_than("1.10")')
dcos_1_9 = pytest.mark.skipif('dcos_version_less_than("1.9")')
dcos_1_8 = pytest.mark.skipif('dcos_version_less_than("1.8")')
dcos_1_7 = pytest.mark.skipif('dcos_version_less_than("1.7")')


def dcos_canonical_version():
    return __canonical_version(shakedown.dcos_version())


def __canonical_version(version):
    index = version.rfind("-dev")
    if index != -1:
        version = version[:index]
    return LooseVersion(version)


def dcos_version_less_than(version):
    return dcos_canonical_version() < LooseVersion(version)


def required_cpus(cpus):
    """ Returns True if the number of available cpus is equal to or greater than
    the cpus.  This is useful in using pytest skipif such as:
    `pytest.mark.skipif('required_cpus(2)')` which will skip the test if
    the number of cpus is not 2 or more.

    :param cpus: the number of required cpus.
    """
    resources = available_resources()
    # reverse logic (skip if less than count)
    # returns True if less than count
    return resources.cpus < cpus


def required_mem(mem):
    """ Returns True if the number of available memory is equal to or greater than
    the mem.  This is useful in using pytest skipif such as:
    `pytest.mark.skipif('required_mem(2)')` which will skip the test if
    the number of mem is not 2m or more.

    :param mem: the amount of required mem in meg.
    """
    resources = available_resources()
    # reverse logic (skip if less than count)
    # returns True if less than count
    return resources.mem < mem


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
