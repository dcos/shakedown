import os
import requests

import dcos

import shakedown as shakedown


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


def master_ip():
    """Returns the public IP address of the DCOS master.
    return: DCOS IP address as a string
    """
    return requests.get(dcos_url() + '/metadata').json()["PUBLIC_IPV4"].strip()
