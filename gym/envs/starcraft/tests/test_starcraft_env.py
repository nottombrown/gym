from gym.envs.StarCraftEnv import StarCraftEnv
from gym.envs.starcraft.starcraft_api_client import StarCraftAPIClient
from gym.envs.starcraft.starcraft_basic_env import StarCraftBasicEnv
from gym.envs.starcraft.tests.helper import StarCraftAPITestCase, TestData


class StarCraftEnvTest(StarCraftAPITestCase):
    """
    We test the private methods of the Env to make sure that the correct arguments are sent
    to our mock API
    """
    def setUp(self):
        self.env = StarCraftBasicEnv()

    def test_init(self):
        self.assertIsNotNone(self.env.id)

    def test_reset(self):
        self.assertIsNotNone(self.env.id)

    def test_step(self):
        self.assertIsNotNone(self.env.id)

    def test_step(self):
        self.assertIsNotNone(self.env.id)

