import os

from dcos import (marathon, mesos, package, util)
from dcos.errors import DCOSException


def package_install(package_name, wait_until_healthy = False):
    """ Install a package via the DCOS library
    """

    config = util.get_config()

    package_version = None
    app_id = package_name

    pkg = package.resolve_package(package_name, config)
    pkg_revision = pkg.latest_package_revision(package_version)
    pkg_json = pkg.package_json(pkg_revision)
    options = pkg.options(pkg_revision, None)
    revision_map = pkg.package_revisions_map()
    package_version = revision_map.get(pkg_revision)
    init_client = marathon.create_client(config)

    package.install_app(pkg, pkg_revision, init_client, options, app_id)

    post_install_notes = pkg_json.get('postInstallNotes')
    if post_install_notes:
        print(post_install_notes)

    return True


def package_installed(package_name):
    """ Check whether a package is currently installed; True = installed, False = nope
    """

    config = util.get_config()
    init_client = marathon.create_client(config)
    installed_apps = package.installed_apps(init_client)

    for app in installed_apps:
        if app['name'] == package_name:
            return True

    return False


def package_uninstall(package_name):
    """ Uninstall a package using the DCOS library
    """

    config = util.get_config()

    package_version = None
    app_id = package_name
    init_client = marathon.create_client(config)
    dcos_client = mesos.DCOSClient()

    package.uninstall_app(package_name, True, app_id, init_client, dcos_client)

    return True
