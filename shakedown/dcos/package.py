import json
import logging
import time

from .marathon import deployment_wait
from .service import delete_persistent_data, wait_for_mesos_task_removal, wait_for_service_tasks_running
from .spinner import pretty_duration, time_wait, TimeoutExpired

from ..clients import cosmos, packagemanager
from ..errors import DCOSException


logger = logging.getLogger(__name__)


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


def _get_service_name(package_name, pkg):
    labels = pkg.marathon_json({}).get('labels')
    if 'DCOS_SERVICE_NAME' in labels:
        return labels['DCOS_SERVICE_NAME']
    else:
        return package_name


def _get_package_manager():
    """ Get an instance of Cosmos with the correct URL.

        :return: Cosmos instance
        :rtype: packagemanager.PackageManager
    """

    return packagemanager.PackageManager(cosmos.get_cosmos_url())


def install_package(
        package_name,
        package_version=None,
        service_name=None,
        options_file=None,
        options_json=None,
        wait_for_completion=False,
        timeout_sec=600,
        expected_running_tasks=0
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
        :param wait_for_completion: whether or not to wait for the app's deployment to complete
        :type wait_for_completion: bool
        :param timeout_sec: number of seconds to wait for task completion
        :type timeout_sec: int
        :param expected_running_tasks: number of service tasks to check for, or zero to disable
        :type expected_task_count: int

        :return: True if installation was successful, False otherwise
        :rtype: bool
    """

    start = time.time()

    if options_file:
        options = _get_options(options_file)
    elif options_json:
        options = options_json
    else:
        options = {}

    package_manager = _get_package_manager()
    pkg = package_manager.get_package_version(package_name, package_version)

    if package_version is None:
        # Get the resolved version for logging below
        package_version = 'auto:{}'.format(pkg.version())

    if service_name is None:
        # Get the service name from the marathon template
        try:
            labels = pkg.marathon_json(options).get('labels')
            if 'DCOS_SERVICE_NAME' in labels:
                service_name = labels['DCOS_SERVICE_NAME']
        except DCOSException:
            pass

    logger.info('\n>>installing %s with service=%s version=%s options=%s',
                package_name, service_name, package_version, options)

    try:
        # Print pre-install notes to console log
        pre_install_notes = pkg.package_json().get('preInstallNotes')
        if pre_install_notes:
            logger.info(pre_install_notes)

        package_manager.install_app(pkg, options, service_name)

        # Print post-install notes to console log
        post_install_notes = pkg.package_json().get('postInstallNotes')
        if post_install_notes:
            logger.info(post_install_notes)

        # Optionally wait for the app's deployment to finish
        if wait_for_completion:
            logger.info("\n>>waiting for %s deployment to complete...", service_name)
            if expected_running_tasks > 0 and service_name is not None:
                wait_for_service_tasks_running(service_name, expected_running_tasks, timeout_sec)

            app_id = pkg.marathon_json(options).get('id')
            deployment_wait(timeout_sec, app_id)
            logger.info('\n>>install completed after %s', pretty_duration(time.time() - start))
        else:
            logger.info('\n>>install started after %s', pretty_duration(time.time() - start))
    except DCOSException as e:
        logger.exception('\n>>')

    return True


def install_package_and_wait(
        package_name,
        package_version=None,
        service_name=None,
        options_file=None,
        options_json=None,
        wait_for_completion=True,
        timeout_sec=600,
        expected_running_tasks=0
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
        timeout_sec,
        expected_running_tasks
    )


def package_installed(package_name, service_name=None):
    """ Check whether the package package_name is currently installed.

        :param package_name: package name
        :type package_name: str
        :param service_name: service_name
        :type service_name: str

        :return: True if installed, False otherwise
        :rtype: bool
    """

    package_manager = _get_package_manager()

    return len(package_manager.installed_apps(package_name, service_name)) > 0


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

    package_manager = _get_package_manager()
    pkg = package_manager.get_package_version(package_name, None)

    try:
        if service_name is None:
            service_name = _get_service_name(package_name, pkg)

        logger.info(">>uninstalling package '%s' with service name '%s'", package_name, service_name)

        package_manager.uninstall_app(package_name, all_instances, service_name)

        # Optionally wait for the service to unregister as a framework
        if wait_for_completion:
            wait_for_mesos_task_removal(service_name, timeout_sec=timeout_sec)
    except DCOSException as e:
        logger.exception('\n>>')

    return True


def uninstall_package_and_wait(
        package_name,
        service_name=None,
        all_instances=False,
        wait_for_completion=True,
        timeout_sec=600
):
    """ Uninstall a package via the DC/OS library and wait for completion

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

    return uninstall_package(
        package_name,
        service_name,
        all_instances,
        wait_for_completion,
        timeout_sec
    )


def uninstall_package_and_data(
        package_name,
        service_name=None,
        role=None,
        principal=None,
        zk_node=None,
        timeout_sec=600):
    """ Uninstall a package via the DC/OS library, wait for completion, and delete any persistent data

        :param package_name: name of the package
        :type package_name: str
        :param service_name: unique service name for the package
        :type service_name: str
        :param role: role to use when deleting data, or <service_name>-role if unset
        :type role: str, or None
        :param principal: principal to use when deleting data, or <service_name>-principal if unset
        :type principal: str, or None
        :param zk_node: zk node to delete, or dcos-service-<service_name> if unset
        :type zk_node: str, or None
        :param wait_for_completion: whether or not to wait for task completion before returning
        :type wait_for_completion: bool
        :param timeout_sec: number of seconds to wait for task completion
        :type timeout_sec: int
    """
    start = time.time()

    if service_name is None:
        pkg = _get_package_manager().get_package_version(package_name, None)
        service_name = _get_service_name(package_name, pkg)
    logger.info('\n>>uninstalling/deleting %s', service_name)

    try:
        uninstall_package_and_wait(package_name, service_name=service_name, timeout_sec=timeout_sec)
    except (DCOSException, ValueError) as e:
        logger.exception('Got exception when uninstalling package, continuing with janitor anyway.')

    data_start = time.time()

    if (not role or not principal or not zk_node) and service_name is None:
        msg = 'service_name must be provided when data params are missing AND the package isn\'t installed'
        raise DCOSException(msg)
    if not role:
        role = '{}-role'.format(service_name)
    if not zk_node:
        zk_node = 'dcos-service-{}'.format(service_name)
    delete_persistent_data(role, zk_node)

    finish = time.time()

    logger.info('\n>>uninstall/delete done after pkg(%s) + data(%s) = total(%s)',
                pretty_duration(data_start - start),
                pretty_duration(finish - data_start),
                pretty_duration(finish - start))


def get_package_repos():
    """ Return a list of configured package repositories
    """

    package_manager = _get_package_manager()
    return package_manager.get_repos()


def package_version_changed_predicate(package_manager, package_name, prev_version):
    """ Returns whether the provided package has a version other than prev_version
    """
    return package_manager.get_package_version(package_name, None) != prev_version


def add_package_repo(
        repo_name,
        repo_url,
        index=None,
        wait_for_package=None,
        expect_prev_version=None):
    """ Add a repository to the list of package sources

        :param repo_name: name of the repository to add
        :type repo_name: str
        :param repo_url: location of the repository to add
        :type repo_url: str
        :param index: index (precedence) for this repository
        :type index: int
        :param wait_for_package: the package whose version should change after the repo is added
        :type wait_for_package: str, or None

        :return: True if successful, False otherwise
        :rtype: bool
    """

    package_manager = _get_package_manager()
    if wait_for_package:
        prev_version = package_manager.get_package_version(wait_for_package, None)
    if not package_manager.add_repo(repo_name, repo_url, index):
        return False
    if wait_for_package:
        try:
            time_wait(lambda: package_version_changed_predicate(package_manager, wait_for_package, prev_version))
        except TimeoutExpired:
            return False
    return True


def remove_package_repo(repo_name, wait_for_package=None):
    """ Remove a repository from the list of package sources

        :param repo_name: name of the repository to remove
        :type repo_name: str
        :param wait_for_package: the package whose version should change after the repo is removed
        :type wait_for_package: str, or None

        :returns: True if successful, False otherwise
        :rtype: bool
    """

    package_manager = _get_package_manager()
    if wait_for_package:
        prev_version = package_manager.get_package_version(wait_for_package, None)
    if not package_manager.remove_repo(repo_name):
        return False
    if wait_for_package:
        try:
            time_wait(lambda: package_version_changed_predicate(package_manager, wait_for_package, prev_version))
        except TimeoutExpired:
            return False
    return True


def remove_package_repo_and_wait(repo_name, wait_for_package):
    """ Remove a repository from the list of package sources, then wait for the removal to complete

        :param repo_name: name of the repository to remove
        :type repo_name: str
        :param wait_for_package: the package whose version should change after the repo is removed
        :type wait_for_package: str

        :returns: True if successful, False otherwise
        :rtype: bool
    """
    return remove_package_repo(repo_name, wait_for_package)


def get_package_versions(package_name):
    """ Returns the list of versions of a given package
        :param package_name: name of the package
        :type package_name: str
    """
    package_manager = _get_package_manager()
    pkg = package_manager.get_package_version(package_name, None)
    return pkg.package_versions()
