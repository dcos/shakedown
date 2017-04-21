"""Utilities for working with authenication and authorization
   Many of the functions here are for DC/OS Enterprise.
"""

from shakedown import *
from urllib.parse import urljoin
from dcos import http
import pytest

from dcos.errors import DCOSHTTPException


def _acl_url():
    return urljoin(dcos_url(), 'acs/api/v1/')


def add_user(uid, password, desc):

    try:
        user_object = {"description": desc, "password": password}
        acl_url = urljoin(_acl_url(), 'users/{}'.format(uid))
        r = http.put(acl_url, json=user_object)
        assert r.status_code == 201
    except DCOSHTTPException as e:
        if e.response.status_code == 409:
            pass
        else:
            raise


def ensure_resource(rid):
    try:
        acl_url = urljoin(_acl_url(), 'acls/{}'.format(rid))
        r = http.put(acl_url, json={'description': 'jope'})
        assert r.status_code == 201
    except DCOSHTTPException as e:
        if e.response.status_code == 409:
            pass
        else:
            raise


def set_user_permission(rid, uid, action='full'):
    rid = rid.replace('/', '%252F')
    # Create ACL if it does not yet exist.
    ensure_resource(rid)

    # Set the permission triplet.
    try:
        usr_url = urljoin(_acl_url(), 'acls/{}/users/{}/{}'.format(rid, uid, action))
        r = http.put(usr_url)
        assert r.status_code == 204
    except DCOSHTTPException as e:
        if e.response.status_code == 409:
            pass
        else:
            raise
