import gym
from gym import spaces
from gym.envs.starcraft.remote_env_api_client import RemoteEnvAPIClient

from gym.envs.starcraft.starcraft_image_file import StarCraftImageFile, \
    starcraft_screen_height, \
    starcraft_screen_width
import numpy as np


class StarCraftEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array']
    }

    # RemoteEnvAPIClient is stateless, so we share it among Env instances
    api_client = RemoteEnvAPIClient()

    def __init__(self):
        self.viewer = None
        self._cached_obs = None # Cache the last observation we've seen

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

        body = self.api_client.create_env()  # Initializes a new episode on the server
        self.id = body["env_id"]
        self._decode_and_cache_raw_observation(body["observation"])

    def _decode_and_cache_raw_observation(self, raw_observation):
        """
        Convert a raw observation into a numpy vector. We cache it to prevent having to do
        additional requests to the API

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

    def _reset(self):
        _, _, body = self.api_client.reset_env(self.id, {
            "map": "StarCraftMining-v0",
        })
        observation = self._decode_and_cache_raw_observation(body["observation"])
        return observation

    def _step(self, action_payload):
        body = self.api_client.step_env(self.id, action_payload)
        observation = self._decode_and_cache_raw_observation(body["observation"])
        return observation, body["reward"], body["done"], {}

    def _get_rgb(self):
        img = StarCraftImageFile.from_np_array(self._cached_obs)
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

    def _close(self):
        self.api_client.close_env(self.id)
