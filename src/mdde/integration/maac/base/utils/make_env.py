from mdde.core import Environment
from mdde.scenario.abc import ABCScenario
from mdde.config import ConfigEnvironment
from mdde.registry.protocol import PRegistryControlClient, PRegistryWriteClient, PRegistryReadClient
from mdde.registry.tcp import RegistryClientTCP

from mdde.integration.maac import MAACMultiAgentEnv


def make_env_tcp(host: str,
                 port: int,
                 env_config: ConfigEnvironment,
                 scenario: ABCScenario,
                 write_stats: bool = True) -> MAACMultiAgentEnv:
    """
    Create an environment connected to the MDDE registry via TCP
    :param write_stats: (optional) If True - MDDE will write additional stats for later analysis. Stats are written in
    the result folder defined in the env_config.
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
    environment = Environment(config=env_config,
                              scenario=scenario,
                              registry_ctrl=ctrl_client,
                              registry_write=write_client,
                              registry_read=read_client,
                              write_stats=write_stats)
    # Re-generate data
    environment.initialize_registry()

    return MAACMultiAgentEnv(environment)
