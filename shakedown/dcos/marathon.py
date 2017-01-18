from dcos import marathon
from shakedown.dcos.spinner import *


def deployment_predicate(app_id=None):
    client = marathon.create_client()
    return len(client.get_deployments()) == 0


def deployment_wait(timeout=120, app_id=None):
    time_wait(lambda: deployment_predicate(app_id),
              timeout)


def delete_all_apps():
    client = marathon.create_client()
    client.remove_group("/")


def delete_all_apps_wait():
    delete_all_apps()
    deployment_wait()


def is_app_healthy(app_id):
    client = marathon.create_client()
    app = client.get_app(app_id)

    if app["healthChecks"]:
        return app["tasksHealthy"] == app["instances"]
    else:
        return app["tasksRunning"] == app["instances"]
