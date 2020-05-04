import os
import argparse
from pathlib import Path

from mdde.core import Environment
from mdde.agent.default import SingleNodeDefaultAgent
from mdde.config import ConfigEnvironment, ConfigRegistry
from mdde.scenario.default import DefaultScenario

from mdde.integration.maac.base import run as maac_run


class MaacSampleDefault():
    """
    A simple example code running MDDE default scenario with the debug configuration (refer to the `./debug` folder in
    the MDDE repo root for more details) with MAAC as the learner
    """

    def __init__(self, args_config):
        """
        Constructor
        :param args_config: Configuration MDDE and MAAC
            Required fields MDDE:
                config.reg_host: TCP host of MDDE registry control API
                config.reg_port: TCP port of MDDE registry control API
                config.registry_config: path to the MDDE registry yaml config containing Data nodes
                config.mdde_temp: path to the folder where MDDE can store temporary files if needed
            Required fields MAAC (unchanged from the original publication):
                config.model_name: Name of directory to store model/training contents
                config.model_dir: Absolute path to the base models store
                config.buffer_length: Replay buffer length
                config.n_episodes: number of episodes
                config.episode_length: Episode length
                config.steps_per-update: Steps per model update
                config.num_updates: Number of updates per update cycle
                config.batch_size: Batch size for training
                config.save_interval: Number of steps before model is saved
                config.pol_hidden-dim
                config.critic_hidden-dim
                config.attend_heads
                config.pi_lr
                config.q_lr
                config.tau
                config.gamma
                config.reward_scale: Max reward value (float)
                config.use-gpu: if True, PyTorch will attempt to utilize the GPU

        """
        self._config = args_config
        """Configuration object containing properties required for both MDDE and MAAC"""

    def run(self):
        # Config
        registry_config = os.path.realpath(self._config.config)
        """Path to MDDE Registry configuration file."""
        # Temp dir
        mdde_temp_dir = os.path.realpath(self._config.env_temp_dir)
        """Path to a folder where MDDE should store its temporary files."""
        os.makedirs(os.path.abspath(mdde_temp_dir), exist_ok=True)
        # Result paths
        result_dir_path_root = Path(self._config.result_dir).resolve()
        result_dir_path_mdde_obj = result_dir_path_root.joinpath("mdde")
        result_dir_path_mdde_obj.mkdir(parents=True, exist_ok=True)
        result_dir_path_mdde = str(result_dir_path_mdde_obj)
        """Path to the folder where MDDE would output the result."""

        mdde_config = ConfigEnvironment(tmp_dir=mdde_temp_dir,
                                        result_dir=result_dir_path_mdde)

        # Registry configuration
        config_container = ConfigRegistry()
        config_container.read(registry_config)
        # Create agents
        agents = list()
        idx = 0
        for node in config_container.get_nodes():
            agents.append(SingleNodeDefaultAgent(agent_name=node.id,
                                                 agent_id=idx,
                                                 data_node_id=node.id,
                                                 write_stats=True,
                                                 allow_do_nothing=True))
            idx += 1

        # Create scenario
        scenario = DefaultScenario(num_fragments=20,
                                   num_steps_before_bench=25,
                                   agents=agents,
                                   benchmark_clients=5)  # Number of YCSB threads

        maac_run(self._config, mdde_config, scenario)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # MDDE Specific
    parser.add_argument('--reg-host',
                        help='MDDE registry host or IP',
                        type=str,
                        default='localhost')
    parser.add_argument('--reg-port',
                        help='MDDE registry control TCP port',
                        type=int,
                        default=8942)

    # next two parameters default values assume MDDE was checked out into the root of this repo
    parser.add_argument('-c', '--config',
                        help='Path to the MDDE registry configuration YAML',
                        type=str,
                        default="../mdde/debug/registry_config.yml")
    parser.add_argument('-t', '--env-temp-dir',
                        help="Directory for temporary files created by the scenario or agents.",
                        type=str,
                        default="../mdde/debug/temp")
    parser.add_argument('-r', '--result-dir',
                        help="Results directory.",
                        type=str,
                        default="../mdde/debug/result")

    # MAAC Specific
    parser.add_argument("--model-name",
                        default="default",
                        help="Name of directory to store model/training contents")
    parser.add_argument("--model-dir",
                        default="./models",
                        help="Path to the base models store")
    parser.add_argument("--buffer-length", default=int(1e6), type=int)
    parser.add_argument("--n-episodes", default=1000, type=int)
    parser.add_argument("--episode-length", default=200, type=int)
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
    parser.add_argument("--reward-scale", default=50000., type=float)
    parser.add_argument("--use-gpu", action='store_true',
                        help="Set this flag for MAAC to utilize GPU if available.")

    args_parsed = parser.parse_args()

    sample = MaacSampleDefault(args_parsed)
    sample.run()
