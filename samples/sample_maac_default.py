import os
import argparse
from typing import Union

from mdde.core import Environment
from mdde.agent.default import DefaultAgent
from mdde.config import ConfigEnvironment, ConfigRegistry
from mdde.scenario.default import DefaultScenario


class MaacSampleDefault():

    def __init__(self, config):
        self.registry_host = config.reg_host
        """MDDE Registry TCP host"""
        self.registry_port = config.reg_port
        """MDDE Registry TCP port"""
        self.registry_config = os.path.realpath(config.reg_config_file)
        """Path to MDDE Registry configuration file"""
        self.mdde_temp_dir = os.path.realpath(config.mdde_temp_dir)
        """Path to a folder where MDDE should store its temporary files"""

        os.makedirs(os.path.abspath(self.mdde_temp_dir), exist_ok=True)

    def run(self):
        mdde_config = ConfigEnvironment(self.mdde_temp_dir)

        # Registry configuration
        config_container = ConfigRegistry()
        config_container.read(self.registry_config)
        # Create agents
        agents = list()
        idx = 0
        for node in config_container.get_nodes():
            agents.append(DefaultAgent(node.id, idx, node.id))
            idx += 1

        # Create scenario
        scenario = DefaultScenario(100, 5, agents)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # MDDE Specific
    parser.add_argument("--registry-host",
                        help="MDDE Registry host",
                        type=str,
                        default="localhost")
    parser.add_argument("--registry-port",
                        help="MDDE Registry port",
                        type=int,
                        default=8942)

    # next two parameters default values assume MDDE was checked out into the root of this repo
    parser.add_argument("--registry-config",
                        help="MDDE Registry configuration YAML",
                        type=str,
                        default="../mdde/debug/registry_config.yml")
    parser.add_argument("--mdde-temp",
                        help="MDDE Temporary files folder.",
                        type=str,
                        default="../mdde/debug/agents")

    # MAAC Specific
    parser.add_argument("--model-name",
                        help="Name of directory to store " +
                             "model/training contents")
    parser.add_argument("--model-dir",
                        default="./models",
                        help="Absolute path to the base models store")
    parser.add_argument("--buffer-length", default=int(1e6), type=int)
    parser.add_argument("--n-episodes", default=50000, type=int)
    parser.add_argument("--episode-length", default=25, type=int)
    parser.add_argument("--steps-per-update", default=100, type=int)
    parser.add_argument("--num-updates", default=4, type=int,
                        help="Number of updates per update cycle")
    parser.add_argument("--batch-size",
                        default=1024, type=int,
                        help="Batch size for training")
    parser.add_argument("--save-interval", default=1000, type=int)
    parser.add_argument("--pol-hidden-dim", default=128, type=int)
    parser.add_argument("--critic-hidden-dim", default=128, type=int)
    parser.add_argument("--attend-heads", default=4, type=int)
    parser.add_argument("--pi-lr", default=0.001, type=float)
    parser.add_argument("--q-lr", default=0.001, type=float)
    parser.add_argument("--tau", default=0.001, type=float)
    parser.add_argument("--gamma", default=0.99, type=float)
    parser.add_argument("--reward-scale", default=100., type=float)
    parser.add_argument("--use-gpu", action='store_true')

    args_parsed = parser.parse_args()
