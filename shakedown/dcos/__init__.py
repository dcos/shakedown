import os
import dcos
import requests

import shakedown


def dcos_url():
    """Return the DCOS URL as configured in the DCOS library. This is
    equivalent to the value of '--dcos_url' passed into Shakedown on the
    command line.
    :return: DCOS cluster URL as a string
    """
    return dcos.util.get_config().get('core.dcos_url')


def dcos_service_url(service):
    """Return the URL of a service running on DCOS, based on the value of
    shakedown.dcos.dcos_url() and the service name.
    :param service: the name of a registered DCOS service, as a string
    :return: the full DCOS service URL, as a string
    """
    return '/'.join([dcos_url(), 'service', service])


def dcos_version():
    """Return the version of the running cluster.
    :return: DC/OS cluster version as a string
    """
    url = "{}/dcos-metadata/dcos-version.json".format(dcos_url())
    response = requests.request('get', url)

    if response.status_code == 200:
        return response.json()['version']
    else:
        return None


def master_ip():
    """Returns the public IP address of the DCOS master.
    return: DCOS IP address as a string
    """
    return dcos.mesos.DCOSClient().metadata().get('PUBLIC_IPV4')


def authenticate(username, password):
    """Authenticate with a DC/OS cluster and return an ACS token.
    return: ACS token
    """

    from six.moves import urllib
    url = urllib.parse.urljoin(dcos_url(), 'acs/api/v1/auth/login')

    creds = {
        'uid': username,
        'password': password
    }

    response = requests.request('post', url, json=creds)

    if response.status_code == 200:
        return response.json()['token']
    else:
        return None
