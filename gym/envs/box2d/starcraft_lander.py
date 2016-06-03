import sys, math
import numpy as np
import zmq

import gym
from gym import spaces

# Rocket trajectory optimization is a classic topic in Optimal Control.
#
# According to Pontryagin's maximum principle it's optimal to fire engine full throttle or
# turn it off. That's the reason this environment is OK to have discreet actions (engine on or off).
#
# Landing pad is always at coordinates (0,0). Coordinates are the first two numbers in state vector.
# Reward for moving from the top of the screen to landing pad and zero speed is about 100..140 points.
# If lander moves away from landing pad it loses reward back. Episode finishes if the lander crashes or
# comes to rest, receiving additional -100 or +100 points. Each leg ground contact is +10. Solved is 200 points.
# Landing outside landing pad is possible. Fuel is infinite, so an agent can learn to fly and then land
# on its first attempt. Please see source code for details.
#
# Too see heuristic landing, run:
#
# python gym/envs/box2d/lunar_lander.py
#
# To play yourself, run:
#
# python examples/agents/keyboard_agent.py StarCraftLander-v0
#
# Created by Oleg Klimov. Licensed on the same terms as the rest of OpenAI Gym.

VIEWPORT_W = 640
VIEWPORT_H = 480


# Proof of concept
context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)

windows_server_2012_url = "tcp://0.tcp.ngrok.io:12635"
socket.connect(windows_server_2012_url)
# socket.connect("tcp://localhost:6666")


class StarCraftLander(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array']
    }

    def __init__(self):
        self.viewer = None

        high = np.array([np.inf]*8)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(-high, high)
        self._reset()

    def _reset(self):
        return self._step(0)[0]

    def _step(self, action):
        assert action in [0,1,2,3], "%r (%s) invalid " % (action,type(action))

        # print action

        if action == 1:
            print("Sending request %s ..." % action)
            socket.send_json("Hello")

            #  Get the reply.
            message = socket.recv()
            print("Received reply %s [ %s ]" % (request, message))

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
            return super(StarCraftLander, self).render(mode=mode)
