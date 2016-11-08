from dcos import marathon
from shakedown.dcos.spinner import *


def deployment_predicate():
    client = marathon.create_client()
    return len(client.get_deployments()) == 0


def deployment_wait(timeout=120):
    time_wait(deployment_predicate, timeout)


def delete_all_apps():
    client = marathon.create_client()
    client.remove_group("/")


def delete_all_apps_wait():
    delete_all_apps()
    deployment_wait()
