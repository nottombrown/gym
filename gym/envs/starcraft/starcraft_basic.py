import sys, math
import numpy as np

import gym
from gym import spaces

from remote_starcraft_game import RemoteStarCraftGame

# To play yourself, run:
#
# python examples/agents/mouse_agent.py StarCraftBasic-v0

VIEWPORT_W = 640
VIEWPORT_H = 480

# Proof of concept - TODO: Massively refactor this

class StarCraftBasic(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array']
    }

    def __init__(self):
        self.viewer = None
        self.game = RemoteStarCraftGame()

        high = np.array([np.inf]*8)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(-high, high)
        self._reset()

    def _reset(self):
        return self._step(0)[0]


    # TODO: Switch this to using numpy actions rather than action payloads
    def _step(self, action_payload):


        # TODO: Re-enable assertions
        # assert action in [0,1,2,3], "%r (%s) invalid " % (action,type(action))

        if action_payload != 0: # 0 is the null action
            self.game.make_action(action_payload)

        observation = np.zeros([8])
        reward = 0
        done = False

        return observation, reward, done, {}

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        from gym.envs.classic_control import rendering
        if self.viewer is None:
            self.viewer = rendering.Viewer(VIEWPORT_W, VIEWPORT_H)
            self.viewer.set_bounds(0, VIEWPORT_W, 0, VIEWPORT_H)

        # Render here

        self.viewer.render()
        if mode == 'rgb_array':
            return self.viewer.get_array()
        elif mode is 'human':
            pass
        else:
            return super(StarCraftBasic, self).render(mode=mode)
