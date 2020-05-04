from typing import Union, Callable, Iterable

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
                 write_stats: bool = True,
                 observation_shaper: Union[None, Callable[[Iterable], Iterable]] = None) -> MAACMultiAgentEnv:
    """
    Create an environment connected to the MDDE registry via TCP.
    :param host: MDDE Registry host.
    :type host: str
    :param port: MDDE Registry port.
    :type port: int
    :param env_config: Environment configurations.
    :type env_config: mdde.config.ConfigEnvironment
    :param scenario: Configured MDDE scenario.
    :param write_stats: (optional) If True - MDDE will write additional stats for later analysis. Stats are written in
    the result folder defined in the env_config.
    :type write_stats: bool
    :param observation_shaper: (optional) Function taking an observation array and reshaping it.
    :type observation_shaper: Union[None, Callable[[Iterable], Iterable]]
    :return: MDDE Environment wrapper for MAAC.
    :rtype: mdde.integration.maac.MAACMultiAgentEnv
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

    return MAACMultiAgentEnv(mdde_env=environment, observation_shaper=observation_shaper)
