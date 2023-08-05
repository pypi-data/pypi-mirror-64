# __init__.py

import logging
import os
import docker
import docker.errors
import time
from typing import List

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


class DockerContainer:

    def __init__(self, connection_string: str = 'tcp://127.0.0.1:2375', detach: bool = False,
                 container_name: str = None, image: str = None, environment: List = None,
                 ports: dict = None):
        """Create a connetion to a running Docker container.

        Args:
            connection_string: URL to the Docker server.
            detach: Run the container in the background (returns a container object, else logs)
            container_name: Running container name.
            image: Docker image name.
            environment: Environment variables to pass to container.
            ports: Exposed port to mop on the container.
        Returns:
            Reference to running Docker container.
        """

        logger.debug(f'Connecting to Docker engine: {connection_string}')
        self.client = docker.DockerClient(base_url=connection_string)
        logger.debug('Connected.')

        self.container = None  # If detached == True, this is the container ID, else it's container logs.

        if image is not None:
            self.pull_image(image)

            if container_name is not None:
                self.run_container(
                    image=image, container_name=container_name, ports=ports, detach=detach, environment=environment
                )

    @property
    def engine_version(self) -> str:
        """Return the Docker server's engine version.

        Returns:
            The engine version.
        """
        try:
            return str(self.client.version()['Components'][0]['Version'])
        except docker.errors.APIError as e:
            raise ConnectionError('An error was encountered when trying to get the Docker server engine version. '
                                  f'This is the error:\n\n{e}')

    def pull_image(self, image: str):
        """Does image exist? If not, download it.

        Args:
            image: Image name, including tag, to search for.
        """
        try:
            self.client.images.get(image)
            logger.debug(f'Found local image: {image}')

        except docker.errors.ImageNotFound:
            try:
                logger.debug(f'Image not found ({image}). Pulling.')
                self.client.images.pull(image)
                logger.debug('Image pulled.')

            except docker.errors.APIError as e:
                raise ConnectionError(f'Problem pulling image ({image}) from Docker hub, Manually pull the image or '
                                      f'confirm credentials and try again.:\n\n{e}')

    def run_container(self, image: str, container_name: str, ports: dict = None, detach: bool = False,
                      environment: List = None):
        """If container is not running, start it.

        Args:
            image: Docker image name.
            container_name: User-defined name for the container.
            ports: Exposed container ports.
            detach: Run the container in the background (returns a container object, else logs)
            environment: Environment variables to pass to container.
        """
        try:
            logger.debug(f'Searching for running container: {container_name}')
            self.client.containers.get(container_name)
            logger.debug('Container is running.')

        except docker.errors.NotFound:
            try:
                self.container = self.client.containers.run(
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

                logger.debug(f'Started {image} container: {container_name}')

            except docker.errors.ImageNotFound as e:
                logger.debug(f'Image not found: {image}\n\n{str(e)}')
            except docker.errors.ContainerError as e:
                logger.debug(f'Container error:\n\n{str(e)}')
            except docker.errors.APIError as e:
                logger.debug(f'Error starting container:\n\n{str(e)}')

    def __del__(self):
        if self.container:
            self.container.stop()
            self.container.remove()
