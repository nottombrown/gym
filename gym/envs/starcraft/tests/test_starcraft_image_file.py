import unittest
from StringIO import StringIO

from numpy import testing as np_test
import numpy as np
from PIL import Image

from gym.envs.starcraft.starcraft_image_file import StarCraftImageFile

class StarCraftImageFileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img = Image.open('gym/envs/starcraft/tests/starcraft_screenshot.scif')
        assert isinstance(cls.img, StarCraftImageFile)

    def test_to_obs(self):
        obs = self.img.to_obs()
        self.assertEqual(obs.shape, (480 * 640,))

    def test_from_np_array(self):
        new_img = StarCraftImageFile.from_np_array(self.img.to_obs())

        # Images are the same
        np_test.assert_equal(new_img.to_obs(), self.img.to_obs())

        # Regression - Palettes are the same
        self.assertEqual(list(self.img.getpalette()), list(new_img.getpalette()))

        # Regression - Bytes are the same when written as a png
        old_bytes = StringIO()
        new_bytes = StringIO()
        self.img.save(old_bytes, format='png')
        new_img.save(new_bytes, format='png')

        self.assertEqual(list(old_bytes), list(new_bytes))

        # Regression - Pixels and palettes are the same
        old_image = Image.open(old_bytes)
        new_image = Image.open(new_bytes)

        self.assertEqual(list(old_image.getdata()), list(new_image.getdata()))
        self.assertEqual(list(old_image.getpalette()), list(new_image.getpalette()))


    def test_to_np_rgb(self):
        np_rgb = self.img.to_np_rgb()
        self.assertEqual(np_rgb.shape, (480, 640, 3))

        # Test that pixels are correct
        first_pixel = np.array([36, 40, 44], dtype=np.uint8)
        np_test.assert_equal(np_rgb[0, 0, :], first_pixel)
    #
    # def test_to_np_rgb_after_vectorizing(self):
    #     # Regression test
    #     new_img = StarCraftImageFile.from_np_array(self.img.to_obs())
    #     np_rgb = new_img.to_np_rgb()
    #
    #     # Test that pixels stay the same after vectorizing
    #     first_pixel = np.array([36, 40, 44], dtype=np.uint8)
    #     np_test.assert_equal(np_rgb[0, 0, :], first_pixel)
