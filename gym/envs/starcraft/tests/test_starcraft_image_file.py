import unittest

from PIL import Image

from gym.envs.starcraft.starcraft_image_file import StarCraftImageFile


class StarCraftImageFileTest(unittest.TestCase):
    def test_open_file(self):
        img = Image.open('gym/envs/starcraft/tests/starcraft_screenshot.scif')
        assert isinstance(img, StarCraftImageFile)
