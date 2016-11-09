import json
import time

from dcos import (cosmospackage, subcommand)
from dcoscli.package.main import get_cosmos_url

import shakedown


def _get_options(options_file=None):
    """ Read in options_file as JSON.

        :param options_file: filename to return
        :type options_file: str

        :return: options as dictionary
        :rtype: dict
    """

    if options_file is not None:
        with open(options_file, 'r') as opt_file:
            options = json.loads(opt_file.read())
    else:
        options = {}
    return options


def _get_cosmos():
    """ Get an instance of Cosmos with the correct URL.

        :return: Cosmos instance
        :rtype: cosmospackage.Cosmos
    """

    return cosmospackage.Cosmos(get_cosmos_url())


def install_package(
        package_name,
        package_version=None,
        service_name=None,
        options_file=None,
        options_json=None,
        wait_for_completion=False,
        timeout_sec=600
):
    """ Install a package via the DC/OS library

        :param package_name: name of the package
        :type package_name: str
        :param package_version: version of the package (defaults to latest)
        :type package_version: str
        :param service_name: unique service name for the package
        :type service_name: str
        :param options_file: filename that has options to use and is JSON format
        :type options_file: str
        :param options_json: dict that has options to use and is JSON format
        :type options_json: dict
        :param wait_for_completion: whether or not to wait for task completion before returning
        :type wait_for_completion: bool
        :param timeout_sec: number of seconds to wait for task completion
        :type timeout_sec: int

        :return: True if installation was successful, False otherwise
        :rtype: bool
    """

    if options_file:
        options = _get_options(options_file)
    elif options_json:
        options = options_json
    else:
        options = {}

    cosmos = _get_cosmos()
    pkg = cosmos.get_package_version(package_name, package_version)
    if service_name is None:
        labels = pkg.marathon_json(options).get('labels')
        if 'DCOS_SERVICE_NAME' in labels:
            service_name = labels['DCOS_SERVICE_NAME']
        else:
            service_name = package_name

    # Install subcommands (if defined)
    if pkg.has_cli_definition():
        print("\n{}installing CLI commands for package '{}'\n".format(shakedown.cli.helpers.fchr('>>'), package_name))
        subcommand.install(pkg)

    print("\n{}installing package '{}' with service name '{}'\n".format(
        shakedown.cli.helpers.fchr('>>'), package_name, service_name)
    )

    # Print pre-install notes to console log
    pre_install_notes = pkg.package_json().get('preInstallNotes')
    if pre_install_notes:
        print(pre_install_notes)

    cosmos.install_app(pkg, options, service_name)

    # Print post-install notes to console log
    post_install_notes = pkg.package_json().get('postInstallNotes')
    if post_install_notes:
        print(post_install_notes)

    # Optionally wait for the service to register as a framework
    if wait_for_completion:
        now = time.time()
        future = now + timeout_sec

        while now < future:
            if shakedown.get_service(service_name):
                return True

            time.sleep(1)
            now = time.time()

        return False

    return True


def install_package_and_wait(
        package_name,
        package_version=None,
        service_name=None,
        options_file=None,
        options_json=None,
        wait_for_completion=True,
        timeout_sec=600
):
    """ Install a package via the DC/OS library and wait for completion
    """

    return install_package(
        package_name,
        package_version,
        service_name,
        options_file,
        options_json,
        wait_for_completion,
        timeout_sec
    )


def package_installed(package_name, service_name=None):
    """ Check whether thea package package_name is currently installed.

        :param package_name: package name
        :type package_name: str
        :param service_name: service_name
        :type service_name: str

        :return: True if installed, False otherwise
        :rtype: bool
    """

    cosmos = _get_cosmos()
    return len(cosmos.installed_apps(package_name, service_name)) > 0


def uninstall_package(
        package_name,
        service_name=None,
        all_instances=False,
        wait_for_completion=False,
        timeout_sec=600
):
    """ Uninstall a package using the DC/OS library.

        :param package_name: name of the package
        :type package_name: str
        :param service_name: unique service name for the package
        :type service_name: str
        :param all_instances: uninstall all instances of package
        :type all_instances: bool
        :param wait_for_completion: whether or not to wait for task completion before returning
        :type wait_for_completion: bool
        :param timeout_sec: number of seconds to wait for task completion
        :type timeout_sec: int

        :return: True if uninstall was successful, False otherwise
        :rtype: bool
    """

    cosmos = _get_cosmos()
    pkg = cosmos.get_package_version(package_name, None)
    if service_name is None:
        labels = pkg.marathon_json({}).get('labels')
        if 'DCOS_SERVICE_NAME' in labels:
            service_name = labels['DCOS_SERVICE_NAME']
        else:
            service_name = package_name

    # Uninstall subcommands (if defined)
    if pkg.has_cli_definition():
        print("\n{}uninstalling CLI commands for package '{}'\n".format(shakedown.cli.helpers.fchr('>>'), package_name))
        subcommand.uninstall(package_name)

    print("\n{}uninstalling package '{}' with service name '{}'\n".format(
        shakedown.cli.helpers.fchr('>>'), package_name, service_name)
    )

    cosmos.uninstall_app(package_name, all_instances, service_name)

    # Optionally wait for the service to unregister as a framework
    if wait_for_completion:
        now = time.time()
        future = now + timeout_sec

        while now < future:
            if not shakedown.get_service(service_name):
                return True

            time.sleep(1)
            now = time.time()

        return False

    return True


def uninstall_package_and_wait(
        package_name,
        service_name=None,
        all_instances=False,
        wait_for_completion=True,
        timeout_sec=600
):
    """ Install a package via the DC/OS library and wait for completion
    """

    return uninstall_package(
        package_name,
        service_name,
        all_instances,
        wait_for_completion,
        timeout_sec
    )


def get_package_repos(
):
    """ Return a list of configured package repositories
    """

    cosmos = _get_cosmos()
    return cosmos.get_repos()


def add_package_repo(
        repo_name,
        repo_url,
        index=None
):
    """ Add a repository to the list of package sources

        :param repo_name: name of the repository to add
        :type repo_name: str
        :param repo_url: location of the repository to add
        :type repo_url: str
        :param index: index (precedence) for this repository
        :type index: int

        :return: True if successful, False otherwise
        :rtype: bool
    """

    cosmos = _get_cosmos()
    return cosmos.add_repo(repo_name, repo_url, index)


def remove_package_repo(
        repo_name
):
    """ Remove a repository from the list of package sources

        :param repo_name: name of the repository to remove
        :type repo_name: str

        :returns: True if successful, False otherwise
        :rtype: bool
    """

    cosmos = _get_cosmos()
    return cosmos.remove_repo(repo_name)
