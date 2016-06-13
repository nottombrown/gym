import unittest

import numpy as np
from numpy import testing as np_test

from gym.envs.starcraft.mouse_keyboard_action import MouseKeyboardAction


class MouseKeyboardActionTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.test_action = MouseKeyboardAction(319, 211, 1, 19, 2)

    def test_to_np(self):
        np_test.assert_equal(self.test_action.to_np(), np.array([319, 211, 1, 19, 2]))

    def test_from_np_array(self):
        desired_dict = {
            "mouse": {
                "x": 319,
                "y": 211,
                "button": 1
            },
            "key": 19,
            "modifiers": 2
        }
        self.assertEqual(self.test_action.to_dict(), desired_dict)
