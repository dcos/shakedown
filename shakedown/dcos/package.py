import time

from dcos import (marathon, mesos, package, util, cosmospackage)
from dcoscli.package.main import _get_cosmos_url
from dcos.errors import DCOSException

import shakedown


def install_package(
    package_name,
    package_version=None,
    app_id=None,
    options_file=None,
    wait_for_completion=False,
    timeout_sec=600
):
    """ Install a package via the DCOS library

        package_name (str): name of the package to install
        package_version (str): version of the package to install (defaults to latest)
        app_id (str): ??
        options_file (?): ??
        wait_for_completion (bool): whether or not to wait for task completion before returning
        timeout_sec (int): time in seconds to wait before timing out
    """

    # Get the dcos configuration object
    config = util.get_config()
    cosmos = cosmospackage.Cosmos(_get_cosmos_url())
    pkg = cosmos.get_package_version(package_name, package_version)

    print("\n" + shakedown.cli.helpers.fchr('>>') + "installing package '" + package_name + "'" + "\n")

    # Print pre-install notes to console log
    pre_install_notes = pkg.package_json().get('preInstallNotes')
    if pre_install_notes:
        print(pre_install_notes)

    cosmos.install_app(pkg, {}, app_id)

    # Print post-install notes to console log
    post_install_notes = pkg.package_json().get('postInstallNotes')
    if post_install_notes:
        print(post_install_notes)

    # Optionally wait for the service to register as a framework
    if wait_for_completion:
        now = time.time()
        future = now + timeout_sec

        while now < future:
            if shakedown.get_service(package_name):
                return True

            time.sleep(1)
            now = time.time()

        return False

    return True


def install_package_and_wait(
    package_name,
    package_version=None,
    app_id=None,
    options_file=None,
    wait_for_completion=True,
    timeout_sec=600
):
    """ Install a package via the DCOS library and wait for completion
    """

    return install_package(
        package_name,
        package_version,
        app_id,
        options_file,
        wait_for_completion,
        timeout_sec
    )


def package_installed(package_name, app_id=None):
    """ Check whether a package is currently installed

        package_name (str): name of the package to check
        app_id (str): ???
    """
    cosmos = cosmospackage.Cosmos(_get_cosmos_url())
    return len(cosmos.installed_apps(package_name, app_id)) > 0


def uninstall_package(
    package_name,
    app_id=None,
    all_instances=False,
    wait_for_completion=False,
    timeout_sec=600
):
    """ Uninstall a package using the DCOS library

        package_name (str): name of the package to uninstall
        app_id (str): ??
        all_instances (bool): ??
        wait_for_completion (bool): whether or not to wait for task completion before returning
        timeout_sec (int): time in seconds to wait before timing out
    """

    config = util.get_config()

    init_client = marathon.create_client(config)
    dcos_client = mesos.DCOSClient()

    print("\n" + shakedown.cli.helpers.fchr('>>') + "uninstalling package '" + package_name + "'" + "\n")

    package.uninstall_app(package_name, True, app_id, init_client, dcos_client)

    # Optionally wait for the service to unregister as a framework
    if wait_for_completion:
        now = time.time()
        future = now + timeout_sec

        while now < future:
            if not shakedown.get_service(package_name):
                return True

            time.sleep(1)
            now = time.time()

        return False

    return True


def uninstall_package_and_wait(
    package_name,
    app_id=None,
    all_instances=False,
    wait_for_completion=True,
    timeout_sec=600
):
    """ Install a package via the DCOS library and wait for completion
    """

    return uninstall_package(
        package_name,
        app_id,
        all_instances,
        wait_for_completion,
        timeout_sec
    )
