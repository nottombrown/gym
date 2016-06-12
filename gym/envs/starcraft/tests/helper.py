import json
import mock
import unittest
import uuid

from gym.envs.starcraft.tests.test_starcraft_image_file import StarCraftImageFileTest
from gym.scoreboard.client.tests.helper import fake_id


class StarCraftAPITestCase(unittest.TestCase):
    def setUp(self):
        super(StarCraftAPITestCase, self).setUp()

        #TODO: correctly patch into our API client
        self.requestor_patcher = mock.patch(
            'gym.envs.starcraft.starcraft_api_client.StarCraftAPIClient')
        requestor_class_mock = self.requestor_patcher.start()
        self.requestor_mock = requestor_class_mock.return_value

    def mock_response(self, res):
        self.requestor_mock.request = mock.Mock(return_value=(res, 'reskey'))


class TestData(object):

    @classmethod
    def create_env_response(cls):
        return cls._success({
                "env_id": fake_id("env"),
                "task": "StarCraftMining-v0",
                "observation": StarCraftImageFileTest.testImage(),
            })
