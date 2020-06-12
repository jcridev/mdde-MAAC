import os
import argparse
from pathlib import Path

from mdde.core import Environment
from mdde.agent.default import SingleNodeDefaultAgent
from mdde.config import ConfigEnvironment, ConfigRegistry
from mdde.registry.workload import EDefaultYCSBWorkload
from mdde.scenario.default import DefaultScenario, DefaultScenarioSimulation

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
        # Workload
        selected_workload: EDefaultYCSBWorkload = EDefaultYCSBWorkload.READ_10000_100000_LATEST_LARGE
        if self._config.light:
            selected_workload: EDefaultYCSBWorkload = EDefaultYCSBWorkload.READ_10000_100000_LATEST

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
                                                 allow_do_nothing=self._config.do_nothing))
            idx += 1

        # Create scenario
        num_fragments: int = 20
        write_stats: bool = True
        if self._config.sim:
            scenario = DefaultScenarioSimulation(num_fragments=num_fragments,
                                                 num_steps_before_bench=self._config.bench_psteps,
                                                 agents=agents,
                                                 benchmark_clients=self._config.bench_clients,
                                                 data_gen_workload=selected_workload,
                                                 bench_workload=selected_workload,
                                                 write_stats=write_stats)  # Number of YCSB threads
        else:
            scenario = DefaultScenario(num_fragments=num_fragments,
                                       num_steps_before_bench=self._config.bench_psteps,
                                       agents=agents,
                                       benchmark_clients=self._config.bench_clients,
                                       data_gen_workload=selected_workload,
                                       bench_workload=selected_workload,
                                       write_stats=write_stats)  # Number of YCSB threads

        # Set multiplier to the sore related term of the default reward function
        scenario.set_storage_importance(self._config.store_m)

        def obs_shaper_2d_box(obs):
            """Reshapes the environment into a form suitable for 2D box. Example 1.
            Note: Guaranteed to work only with the Default agent - Default scenario combination."""
            # Resulted shape (Example for default scenario and default single-node agent: 2 agents, 5 fragments):
            # a_1: [0-4(allocation) 5-9(popularity) 10-14(ownership binary flag)]
            # a_2: [0-4(allocation) 5-9(popularity) 10-14(ownership binary flag)]
            # Hint: 2D array where rows are agents, and attributes in columns are as shown above.
            return obs.reshape((obs.shape[0], obs.shape[1] * obs.shape[2]), order='F')

        def obs_shaper_flat_box(obs):
            """Reshapes the environment into a form suitable for 2D 'flat' box. Example 2.
            Note: Guaranteed to work only with the Default agent - Default scenario combination."""
            # Resulted shape (Example for default scenario and default single-node agent: 2 agents, 5 fragments):
            # [0-4(a_1: allocation) 5-9(a_1: popularity) 10-14(a_1: ownership binary flag)
            #  15-19(a_2: allocation) 20-24(a_2: popularity) 25-29(a_2: ownership binary flag)]
            return obs.reshape((obs.shape[0], obs.shape[1] * obs.shape[2]), order='F')\
                      .reshape((obs.shape[0] * obs.shape[1] * obs.shape[2]), order='C')

        maac_run(config=self._config, mdde_config=mdde_config, scenario=scenario,
                 write_stats=True,
                 observation_shaper=obs_shaper_flat_box)


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
    parser.add_argument("--episode-length", default=1001, type=int)
    parser.add_argument("--steps-per-update", default=100, type=int)
    parser.add_argument("--num-updates", default=4, type=int,
                        help="Number of updates per update cycle")
    parser.add_argument("--batch-size",
                        default=1024, type=int,
                        help="Batch size for training")
    parser.add_argument("--save-interval", default=1000, type=int)
    parser.add_argument("--pol-hidden-dim", default=240, type=int)
    parser.add_argument("--critic-hidden-dim", default=240, type=int)
    parser.add_argument("--attend-heads", default=4, type=int)
    parser.add_argument("--pi-lr", default=0.001, type=float)
    parser.add_argument("--q-lr", default=0.001, type=float)
    parser.add_argument("--tau", default=0.001, type=float)
    parser.add_argument("--gamma", default=0.99, type=float)
    parser.add_argument("--reward-scale", default=10000., type=float)
    parser.add_argument("--use-gpu", action='store_true',
                        help="Set this flag for MAAC to utilize GPU if available.")

    # - MDDE scenario
    # -- Do-nothing action
    parser.add_argument('--do-nothing',
                        dest='do_nothing',
                        action='store_true',
                        help='(Default) Enable the "do nothing" action for agents.')
    parser.add_argument('--no-do-nothing',
                        dest='do_nothing',
                        action='store_false',
                        help='Disable the "do nothing" action for agents.')
    parser.set_defaults(do_nothing=True)

    parser.add_argument('--bench-psteps',
                        help='Frequency of benchmark execution (execute every N steps).',
                        type=int,
                        default=25)

    parser.add_argument('--store-m',
                        help='Importance multiplier for the storage term of the default reward function.'
                             '0.0 - ignore (agents are allowed to hoard everything with no repercussions)',
                        type=float,
                        default=0.5)

    parser.add_argument('--bench-clients',
                        help='Number of benchmark clients.',
                        type=int,
                        default=50)

    parser.add_argument('--sim',
                        help='Simulated benchmark (except the first run).',
                        action='store_true')

    parser.add_argument('--light',
                        help='Execute corresponding "light" workload.',
                        action='store_true')

    args_parsed = parser.parse_args()

    sample = MaacSampleDefault(args_parsed)
    sample.run()
