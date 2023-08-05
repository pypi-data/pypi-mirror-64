# __init__.py

import logging
import os
import docker
import docker.errors
import time
from typing import List, Union, Container

logger = logging.getLogger(__name__)


class Docker:

    def _init__(self):
        """Methods for working inside a Docker container.

        Attributes:
            self.secrets_dir: Directory for Docker secrets.
            self.config_dir: Directory for Docker configs.
        """

        self.secrets_dir: str = '/run/secrets'
        self.config_dir: str = '/run/secrets'

        self.__logger = logging.getLogger(__name__)

    @property
    def secret_list(self):
        """
        Returns:
            A list of secrets
        """
        return os.listdir(self.secrets_dir)

    @property
    def config_list(self):
        """
        Returns:
            A list of configs
        """
        return os.listdir(self.secrets_dir)

    def get_secret(self, secret_name):
        """Retrieve the value of a Docker secret.

        Args:
            secret_name: The name of the secret to retrieve the value from.
        Returns:
            The value of the secret
        """

        with open(f'{self.secrets_dir}/{secret_name}', 'r') as fp:
            secret_value = fp.read()

        return secret_value

    def get_config(self, config_name):
        """Retrieve the value of a Docker config.

        Args:
            config_name: The name of the config to retrieve the value from.
        Returns:
            The value of the config
        """

        with open(f'{self.config_dir}/{config_name}', 'r') as fp:
            config_value = fp.read()

        return config_value


def create_container(connection_string: str = 'tcp://127.0.0.1:2375', detach: bool = False,
                     container_name: str = None, image: str = None, environment: List = None,
                     ports: dict = None) -> Union[Container, None, bytes]:
    """Create a connetion to a running Docker container.

    Args:
        connection_string: URL to the Docker server.
        detach: Run the containre in the background (returns a container object, else logs)
        container_name: Running container name.
        image: Docker Hub image name.
        environment: Environment variables to pass to container.
        ports: Exposed port to mop on the container.
    Returns:
        Reference to running Docker container.
    """

    # Docker connection
    logger.debug('Connecting to Docker engine.')
    client = docker.DockerClient(base_url=connection_string)
    logger.debug('Connected.')

    # Docker image
    try:
        logger.debug(f'Searching for local image: {image}')
        client.images.get(image)

    except docker.errors.ImageNotFound:

        try:
            logger.debug(f'Image not found.  Pulling.')
            client.images.pull(image)
            logger.debug('Image pulled.')

        except docker.errors.APIError as error:
            logger.debug(f'Problem pulling image from Docker hub: {image}')
            logger.debug('Error: ', error)
            logger.debug('Manually pull the image or confirm credentials and try again.')
            exit(0)

    logger.debug('Local image found.')

    # Docker container
    try:
        logger.debug(f'Searching for running container: {container_name}')
        client.containers.get(container_name)

    except docker.errors.NotFound:

        try:
            container = client.containers.run(
                image,
                name=container_name,
                detach=detach,
                remove=True,  # Delete the container when it is stopped.
                environment=environment,
                ports=ports  # Expose the container's SFTP port.
            )

            # Wait for container services to start
            logger.debug('Sleeping for 8 seconds to give container services time to start.')
            time.sleep(8)

            logger.debug(f'Running {image} container: {container}')
            return container

        except docker.errors.ImageNotFound:
            logger.debug(f'Image not found: {image}')
        except docker.errors.ContainerError as error:
            logger.debug('Container error: ', str(error))
        except docker.errors.APIError as error:
            logger.debug('Error starting container: ', str(error))
