"""Utilities for work with docker commands and images"""

import json
import os

from datetime import timedelta
import shakedown

from dcos import marathon


def create_docker_credentials_file(
        username,
        password,
        file_name='docker.tar.gz'):
    """ Create a docker credentials file.
        Docker username and password are used to create a `{file_name}`
        with `.docker/config.json` containing the credentials.

        :param username: docker username
        :type username: str
        :param password: docker password
        :type password: str
        :param file_name: credentials file name `docker.tar.gz` by default
        :type file_name: str
    """

    import base64
    auth_hash = base64.b64encode(
        '{}:{}'.format(username, password).encode()).decode()

    config_json = {
        "auths": {
            "https://index.docker.io/v1/": {"auth": auth_hash}
        }
    }

    config_json_filename = 'config.json'
    # Write config.json to file
    with open(config_json_filename, 'w') as f:
        json.dump(config_json, f, indent=4)

    try:
        # Create a docker.tar.gz
        import tarfile
        with tarfile.open(file_name, 'w:gz') as tar:
            tar.add(config_json_filename, arcname='.docker/config.json')
            tar.close()
    except Exception as e:
        print('Failed to create a docker credentils file {}'.format(e))
        raise e
    finally:
        os.remove(config_json_filename)


def __distribute_docker_credentials_file(file_name='docker.tar.gz'):
    """ Create and copy docker credentials file to passed `{agents}`.
        Used to access private docker repositories in tests.
    """
    # Upload docker.tar.gz to all private agents
    for host in shakedown.get_private_agents():
        shakedown.copy_file(host, file_name)


def distribute_docker_credentials_to_private_agents(
        username,
        password,
        file_name='docker.tar.gz'):
    """ Create and distributes a docker credentials file to all private agents

        :param username: docker username
        :type username: str
        :param password: docker password
        :type password: str
        :param file_name: credentials file name `docker.tar.gz` by default
        :type file_name: str
    """

    create_docker_credentials_file(username, password, file_name)

    try:
        __distribute_docker_credentials_file()
    finally:
        os.remove(file_name)


def prefetch_docker_image_on_private_agents(
        image,
        timeout=timedelta(minutes=5).total_seconds()):
    """ Given a docker image. An app with the image is scale across the private
        agents to ensure that the image is prefetched to all nodes.

        :param image: docker image name
        :type image: str
        :param timeout: timeout for deployment wait in secs (default: 5m)
        :type password: int
    """
    agents = len(shakedown.get_private_agents())
    app = {
        "id": "/prefetch",
        "instances": agents,
        "container": {
            "type": "DOCKER",
            "docker": {"image": image}
        },
        "cpus": 0.1,
        "mem": 128
    }

    client = marathon.create_client()
    client.add_app(app)

    shakedown.deployment_wait(timeout)

    shakedown.delete_all_apps()
    shakedown.deployment_wait(timeout)
