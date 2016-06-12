import gym
from gym import spaces
from gym.envs.starcraft.starcraft_image_file import StarCraftImageFile, \
    starcraft_screen_height, \
    starcraft_screen_width
from starcraft_api_client import StarCraftAPIClient
import numpy as np
# To play yourself, run:
#
# python examples/agents/mouse_keyboard_agent.py StarCraftBasic-v0

class StarCraftBasicEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array']
    }

    def __init__(self):
        self.viewer = None
        self._obs = None # Cache the last observation we've seen

        self.game_client = StarCraftAPIClient()
        self.game_client.reset()  # Initializes a new episode on the server

        self.action_space = spaces.Discrete(4)

        # We use HighLow subspaces because they allow various ranges
        action_subspaces = [
            [[0, starcraft_screen_height, 0]],  # Mouse Y coordinate
            [[0, starcraft_screen_width, 0]],  # Mouse X coordinate
            [[0, 2, 0]],  # Mouse button is one of [off, left, right]
            [[0, 40, 0]],  # There are 36 alphanumerics, plus [tab, space, esc, enter]
            [[0, 7, 0]]   # Each of the three modifiers [shift, control, alt] can be pressed
        ]
        joint_subspaces = sum(action_subspaces, [])
        self.action_space = spaces.HighLow(np.matrix(joint_subspaces))

        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(starcraft_screen_height,
                                                   starcraft_screen_width))
        self._reset()

    def _reset(self):
        return self._step(0)[0]

    def _step(self, action_payload):
        screen_buffer_obs, reward, done, info = self.game_client.step(action_payload)

        observation = StarCraftImageFile.from_screen_buffer(screen_buffer_obs).to_obs()
        self._obs = observation

        return observation, reward, done, info

    def _get_rgb(self):
        img = StarCraftImageFile.from_np_array(self._obs)
        return img.to_np_rgb()

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        if mode == 'rgb_array':
            return self._get_rgb()
        elif mode == 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(self._get_rgb())
