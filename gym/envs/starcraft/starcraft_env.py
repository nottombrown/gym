import numpy as np

import gym
from gym import spaces
from gym.envs.starcraft.mouse_keyboard_action import MouseKeyboardAction
from gym.envs.starcraft.remote_env_api_client import RemoteEnvAPIClient
from gym.envs.starcraft.starcraft_image_file import StarCraftImageFile, \
    starcraft_screen_height, \
    starcraft_screen_width


class StarCraftEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array']
    }

    api_client = RemoteEnvAPIClient()  # share one client among Env instances

    def __init__(self):
        self.viewer = None
        self._cached_obs = None  # Cache the last observation we've seen

        # We use HighLow subspaces because they let us combine various ranges
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

        response = self.api_client.create_env()  # Create a new env on the server
        self.id = response["env_id"]
        self._decode_and_cache_raw_observation(response["observation"])

    def _decode_and_cache_raw_observation(self, raw_observation):
        """
        Convert a raw observation into a numpy vector. We cache it to prevent having to do
        additional requests to the API when rendering

        Args:
            raw_observation: A base-64 encoding of a StarCraft screendump

        Returns:
            A 480 x 640 matrix of uint8s representing a screen dump from a starcraft game
        """
        # Decode the screenbuffer into an observation
        img = StarCraftImageFile.from_b64_screen_buffer(raw_observation)
        observation = img.to_obs()
        self._cached_obs = observation
        return observation

    def _get_rgb(self):
        img = StarCraftImageFile.from_np_array(self._cached_obs)
        return img.to_np_rgb()

    def _step(self, action):
        mouse_keyboard_action = MouseKeyboardAction.from_np(action)
        response = self.api_client.step_env(self.id, mouse_keyboard_action.to_dict())
        observation = self._decode_and_cache_raw_observation(response["observation"])
        return observation, response["reward"], response["done"], {}

    def _reset(self):
        new_environment_params = {
            "map": "StarCraftMining-v0",
        }

        response = self.api_client.reset_env(self.id, new_environment_params)
        observation = self._decode_and_cache_raw_observation(response["observation"])
        return observation

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

    def _close(self):
        self.api_client.close_env(self.id)
