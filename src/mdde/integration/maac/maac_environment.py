from typing import Dict, Tuple, List

import numpy as np

from mdde.core import Environment


class MAACMultiAgentEnv:

    def __init__(self, mdde_env: Environment):
        if mdde_env is None:
            raise TypeError("mdde_env can't be None")
        self._env = mdde_env

    def reset(self) -> List[np.ndarray]:
        """
        Reset the environment and return new observations for each agent
        :return: Observations: dictionary containing observations for each array
        """
        obs = self._env.reset()
        obs_n = list()
        for k in sorted(obs):
            obs_n.append(obs[k].astype(np.float32).flatten())
        return obs_n

    def step(self, action_list: List[List[np.ndarray]]) -> Tuple[List[np.ndarray],
                                                                 List[float],
                                                                 List[bool],
                                                                 List[Dict]]:
        """
        Make step, return observations, rewards, done flags, and info per agent
        :param action_list: Dictionary of action id per
        :return:
        """
        agents = self._env.agents
        env_actions: List[np.ndarray] = action_list[0]  # MDDE does not support parallel environments
        discrete_actions = {}
        for a in agents:
            a_act = env_actions[a.id]
            a_idx = np.argmax(a_act)
            discrete_actions[a.id] = a_idx
        obs, reward = self._env.step(discrete_actions)
        obs_n = list()
        reward_list = list()
        done_list = list()
        info_list = list()
        for k in sorted(obs):
            obs_n.append(obs[k].astype(np.float32).flatten())
            reward_list.append(reward[k])
            done_list[k] = False  # TODO: real dictionary of the terminal states
            info_list[k] = {}

        return obs_n, reward_list, done_list, info_list
