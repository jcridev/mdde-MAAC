from typing import Dict, Tuple, List, Union, Callable

import numpy as np
from gym.spaces import Box, Discrete
from mdde.agent.abc import ABCAgent

from mdde.core import Environment


class MAACMultiAgentEnv:

    def __init__(self,
                 mdde_env: Environment,
                 observation_shaper: Union[None, Callable[[np.ndarray], np.ndarray]] = None):
        """
        Initialize MAAC specific environment.
        :param mdde_env: MDDE Environment.
        :type mdde_env: mdde.core.Environment
        :param observation_shaper: (optional) If specified, will be used for re-shaping the observations,
        otherwise the observations are flattened.
        :type observation_shaper: None or Callable[[np.ndarray], np.ndarray]
        """
        if mdde_env is None:
            raise TypeError("mdde_env can't be None")
        self._env = mdde_env
        """MDDE Environment instance."""

        self._observation_shaper = observation_shaper
        """Re-shaper of the environment."""

    def reset(self) -> List[np.ndarray]:
        """
        Reset the environment and return new observations for each agent
        :return: Observations: dictionary containing observations for each array
        """
        obs = self._env.reset()
        obs_n = list()
        for k in sorted(obs):
            obs_n.append(self._shape_obs(obs[k]))
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
        obs, reward, done = self._env.step(discrete_actions)
        obs_n = list()
        reward_list = list()
        done_list = list()
        info_list = list()
        for k in sorted(obs):
            obs_n.append(self._shape_obs(obs[k]))
            reward_list.append(reward[k])
            done_list.append(done[k])
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
            obs_n.append(self._box_obs(env_obs_space[k]))
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

    def _shape_obs(self, agent_obs: np.ndarray) -> np.ndarray:
        """
        Reshape observations by either using the custom :func:`self.observation_shaper` or :func:`np.flatten()`.
        :param agent_obs: Observations as returned by the scenario.
        :type agent_obs: np.ndarray
        :return: Reshaped obsevations
        :rtype: np.ndarray
        """
        if self._observation_shaper:
            v_float = self._observation_shaper(agent_obs)
        else:
            v_float = agent_obs.astype(np.float64).flatten()
        return v_float

    def _box_obs(self, agent_obs: np.ndarray) -> Box:
        """
        Reshape observations and wrap into the Gym.Box shape.
        :param agent_obs: Observations as returned by the scenario.
        :type agent_obs: np.ndarray
        :return: 2D Box.
        :rtype: gym.spaces.box.Box
        """
        v_float = self._shape_obs(agent_obs)
        return Box(low=0.0, high=1.0, shape=v_float.shape)
