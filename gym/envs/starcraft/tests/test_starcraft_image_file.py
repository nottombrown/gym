import unittest
from numpy import testing as np_test
import numpy as np
from PIL import Image

from gym.envs.starcraft.starcraft_image_file import StarCraftImageFile

class StarCraftImageFileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Read the test image into memory, we use it for the rest of the tests
        cls.img = Image.open('gym/envs/starcraft/tests/starcraft_screenshot.scif')
        assert isinstance(cls.img, StarCraftImageFile)

    def test_to_obs(self):
        obs = self.img.to_obs()
        self.assertEqual(obs.shape, (480, 640))

    def test_from_np_array(self):
        new_img = StarCraftImageFile.from_np_array(self.img.to_obs())

        # Images are the same
        np_test.assert_equal(new_img.to_obs(), self.img.to_obs())

    def test_palette_serialization(self):
        new_img = StarCraftImageFile.from_np_array(self.img.to_obs())

        # Regression - Make sure that palettes are the same
        self.assertEqual(list(self.img.getpalette()), list(new_img.getpalette()))

    def test_to_np_rgb(self):
        np_rgb = self.img.to_np_rgb()
        self.assertEqual(np_rgb.shape, (480, 640, 3))

        # Test that pixels are correct
        first_pixel = np.array([36, 40, 44], dtype=np.uint8)
        np_test.assert_equal(np_rgb[0, 0, :], first_pixel)
