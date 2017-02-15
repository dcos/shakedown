from distutils.version import LooseVersion
from dcos import marathon
from shakedown.dcos.spinner import *

import pytest


marathon_1_3 = pytest.mark.skipif('marthon_version_less_than("1.3")')
marathon_1_4 = pytest.mark.skipif('marthon_version_less_than("1.4")')
marathon_1_5 = pytest.mark.skipif('marthon_version_less_than("1.5")')


def marathon_version():
    client = marathon.create_client()
    about = client.get_about()
    # 1.3.9 or 1.4.0-RC8
    return LooseVersion(about.get("version"))


def marthon_version_less_than(version):
    return marathon_version() < LooseVersion(version)

def deployment_predicate(app_id=None):
    return len(marathon.create_client().get_deployments(app_id)) == 0


def deployment_wait(timeout=120, app_id=None):
    time_wait(lambda: deployment_predicate(app_id),
              timeout)


def delete_app(app_id, force=True):
    marathon.create_client().remove_app(app_id, force=force)


def delete_app_wait(app_id, force=True):
    delete_app(app_id, force)
    deployment_wait(app_id=app_id)


def delete_all_apps(force=True):
    marathon.create_client().remove_group("/", force=force)


def delete_all_apps_wait(force=True):
    delete_all_apps(force=force)
    deployment_wait()


def is_app_healthy(app_id):
    app = marathon.create_client().get_app(app_id)
    if app["healthChecks"]:
        return app["tasksHealthy"] == app["instances"]
    else:
        return app["tasksRunning"] == app["instances"]
