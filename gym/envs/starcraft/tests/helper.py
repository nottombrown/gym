import json
import mock
import unittest
import uuid

from gym.envs.starcraft.tests.test_starcraft_image_file import StarCraftImageFileTest
from gym.scoreboard.client.tests.helper import fake_id


class RemoteEnvAPITestCase(unittest.TestCase):
    def setUp(self):
        super(RemoteEnvAPITestCase, self).setUp()
        self.api_client_patcher = mock.patch(
            'gym.envs.starcraft.remote_env_api_client.RemoteEnvAPIClient')

        api_client_class_mock = self.api_client_patcher.start()
        self.api_client_mock = api_client_class_mock.return_value

    def mock_response(self, res):
        self.api_client_mock.request = mock.Mock(return_value=(res, 'reskey'))

class TestData(object):

    @classmethod
    def create_env_response(cls):
        return {
                "env_id": fake_id("env"),
                "task": "StarCraftMining-v0",
                "observation": StarCraftImageFileTest.testImage(),
            }
