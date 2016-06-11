import numpy as np
import gym
from gym import spaces
from base64 import b64decode
from StringIO import StringIO
from PIL import Image
from gym.envs.starcraft.starcraft_image_plugin import StarCraftImageFile, _SCIF_HEADER
from PIL.PngImagePlugin import PngImageFile

from remote_starcraft_game_client import RemoteStarCraftGameClient

# To play yourself, run:
#
# python examples/agents/mouse_keyboard_agent.py StarCraftBasic-v0


with open("/tmp/starcraft.scif.base64", 'r') as b64_scif:
    scif_bytes = b64decode(b64_scif.read())

stream = StringIO(_SCIF_HEADER + scif_bytes)

im = Image.open(stream)

class StarCraftBasicEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array']
    }

    def __init__(self):
        self.viewer = None
        self.screen_height = 480
        self.screen_width = 640
        self._obs = None # Cache the last observation we've seen

        self.game = RemoteStarCraftGameClient()
        self.game.reset()  # Initializes a new episode on the server

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

        # if action_payload != 0: # 0 is the null action

        observation, reward, done, info = self.game.step(action_payload)
        self._obs = observation

        return observation, reward, done, info

    def _get_rgb(self):
        # img = StarCraftImageFile()
        # img.frombytes(bytearray(self._obs.tolist()))

        assert isinstance(im, StarCraftImageFile)

        png_stream = StringIO()
        im.save(png_stream, format='png')

        png_image = Image.open(png_stream)
        assert isinstance(png_image, PngImageFile)
        png_rgb = png_image.convert('RGB')
        pixel = png_rgb.getpixel((0, 0))
        assert pixel == (36, 40, 44)

        import numpy as np

        # 307200 tuples of (R, G, B)
        pixels = np.array(png_rgb.getdata(), dtype=np.uint8)
        reshaped = pixels.reshape([480, 640, 3])

        return reshaped

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
