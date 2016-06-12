import json

import mock
import unittest
import uuid

from gym.envs.starcraft.tests.test_starcraft_image_file import StarCraftImageFileTest


def fake_id(prefix):
    entropy = ''.join([a for a in str(uuid.uuid4()) if a.isalnum()])
    return '{}_{}'.format(prefix, entropy)

class StarCraftAPITestCase(unittest.TestCase):
    def setUp(self):
        super(StarCraftAPITestCase, self).setUp()
        self.requestor_patcher = mock.patch('gym.scoreboard.client.api_requestor.APIRequestor')
        requestor_class_mock = self.requestor_patcher.start()
        self.requestor_mock = requestor_class_mock.return_value

    def mock_response(self, res):
        self.requestor_mock.request = mock.Mock(return_value=(res, 'reskey'))

class TestData(object):

    @classmethod
    def _success(cls, body):
        return (
            "200",
            json.dumps({}),
            json.dumps(body)
        )

    @classmethod
    def create_env_response(cls):
        return cls._success({
                "env_id": "env_IjWc0oom6G3sZbUp",
                "task": "StarCraftMining-v0",
                "observation": StarCraftImageFileTest.testImage(),
            })