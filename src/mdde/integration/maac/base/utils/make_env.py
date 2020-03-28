from mdde.core import Environment
from mdde.scenario.abc import ABCScenario
from mdde.config import ConfigEnvironment
from mdde.registry.protocol import PRegistryControlClient, PRegistryWriteClient, PRegistryReadClient
from mdde.registry.tcp import RegistryClientTCP

from mdde.integration.maac import MAACMultiAgentEnv


def make_env_tcp(host: str,
                 port: int,
                 env_config: ConfigEnvironment,
                 scenario: ABCScenario) -> MAACMultiAgentEnv:
    """
    Create an environment connected to the MDDE registry via TCP
    :param host: MDDE Registry host
    :param port: MDDE Registry port
    :param env_config: Environment configurations
    :param scenario: Configured MDDE scenario
    :return: MDDE Environment wrapper for MAAC
    """
    # Create Registry client
    tcp_client = RegistryClientTCP(host, port)
    read_client: PRegistryReadClient = tcp_client
    write_client: PRegistryWriteClient = tcp_client
    ctrl_client: PRegistryControlClient = tcp_client

    # Create environment
    environment = Environment(env_config, scenario, ctrl_client, write_client, read_client)
    # Re-generate data
    environment.initialize_registry()

    return MAACMultiAgentEnv(environment)
