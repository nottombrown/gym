from gym.envs.starcraft.starcraft_basic_env import StarCraftBasicEnv
from gym.envs.starcraft.tests.helper import RemoteEnvAPITestCase, TestData


class StarCraftEnvTest(RemoteEnvAPITestCase):
    """
    We test the private methods of the Env to make sure that the correct arguments are sent
    to our mock API
    """
    def setUp(self):
        super(StarCraftEnvTest, self).setUp()

        # Create an env
        response = TestData.create_env_response()
        self.mock_response(response)
        self.env = StarCraftBasicEnv()

    def test_create(self):
        self.request_mock.assert_called_once()
        self.assertIsNotNone(self.env.id)

    def test_step(self):
        response = TestData.step_env_response()
        self.mock_response(response)
        self.env.step(self.env.action_space.sample())
        self.request_mock.assert_called_once()

    def test_reset(self):
        response = TestData.reset_env_response()
        self.mock_response(response)
        self.env.reset()
        self.request_mock.assert_called_once()

    def test_close(self):
        response = TestData.close_env_response()
        self.mock_response(response)
        self.env.close()
        self.request_mock.assert_called_once()


