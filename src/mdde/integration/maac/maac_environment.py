from typing import Dict, Tuple, List

import numpy as np
from gym.spaces import Box, Discrete
from mdde.agent.abc import ABCAgent

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
        discrete_actions = {}
        for a in agents:
            a_act = action_list[a.id]
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
            done_list.append(False)  # TODO: real dictionary of the terminal states
            info_list.append({})

        return obs_n, reward_list, done_list, info_list

    @property
    def observation_space(self) -> List[Box]:
        """
        Environment observation space shape
        :return: Dictionary containing the shape of the observation space per agent
        """
        obs_n = list()
        env_obs_space = self._env.observation_space
        for k in sorted(env_obs_space):
            v_float = env_obs_space[k].astype(np.float32).flatten()
            obs_n.append(Box(low=0.0, high=1.0, shape=v_float.shape))
        return obs_n

    @property
    def action_space(self) -> List[Discrete]:
        """
        Environment action space shape
        :return: Dictionary containing the shape of the action space per agent
        """
        act_n: List[Discrete] = list()
        env_act_space = self._env.action_space
        for k in sorted(env_act_space):
            act_n.append(Discrete(env_act_space[k]))
        return act_n

    @property
    def agents(self) -> Tuple[ABCAgent]:
        """
        Agents
        :return: Agents declared in the environment
        """
        return self._env.agents

    def close(self) -> None:
        """
        A stub for disposing the environment.
        """
        pass
