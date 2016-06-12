from mock import MagicMock

from gym.envs.starcraft import StarCraftEnv
from gym.envs.starcraft.remote_env_api_client import RemoteEnvAPIClient
from gym.envs.starcraft.starcraft_basic_env import StarCraftBasicEnv
from gym.envs.starcraft.tests.helper import RemoteEnvAPITestCase, TestData


class StarCraftEnvTest(RemoteEnvAPITestCase):
    """
    We test the private methods of the Env to make sure that the correct arguments are sent
    to our mock API
    """
    def setUp(self):
        super(StarCraftEnvTest, self).setUp()

    def test_init(self):
        response = TestData.create_env_response()
        self.mock_response(response)

        self.env = StarCraftBasicEnv()
        self.request_mock.assert_called_once()
        self.assertIsNotNone(self.env.id)

    # def test_reset(self):
    #     self.assertIsNotNone(self.env.id)
    #
    # def test_step(self):
    #     self.assertIsNotNone(self.env.id)
    #
    # def test_step(self):
    #     self.assertIsNotNone(self.env.id)

