import unittest

import mock

from gym.envs.starcraft.tests.test_starcraft_image_file import StarCraftImageFileTest
from gym.scoreboard.client.tests.helper import fake_id


class RemoteEnvAPITestCase(unittest.TestCase):
    """
    Patches RemoteEnvAPIClient so that requests always go through a mock RemoteEnvAPIRequestor
    """
    def setUp(self):
        super(RemoteEnvAPITestCase, self).setUp()

        api_request_patcher = mock.patch(
            'gym.envs.starcraft.remote_env_api_requestor.RemoteEnvAPIRequestor')
        self.requestor_class_mock = api_request_patcher.start()

        self.last_api_request = None

    def mock_response(self, response):
        """
        Mock out the next response to return from RemoteEnvAPIRequestor.request

        Requests will be logged into self.last_api_request

        Args:
            response: A (status, headers_dict, body_dict) tuple to return next time we make
             a request
        """
        test_case = self

        def _record_api_request_and_return_mock_response(endpoint, headers, body):
            test_case.last_api_request = (endpoint, headers, body)
            return response

        self.request_mock = mock.Mock(side_effect=_record_api_request_and_return_mock_response)
        self.requestor_class_mock.request = self.request_mock


class TestData(object):

    @classmethod
    def headers(cls):
        return {
            "request_id": fake_id("request")
        }

    @classmethod
    def create_env_response(cls):
        return (
            "200",
            cls.headers(),
            {
                "env_id": fake_id("env"),
                "task": "StarCraftMining-v0",
                "observation": StarCraftImageFileTest.test_image().to_b64_screen_buffer()
            })

    @classmethod
    def step_env_response(cls):
        return (
            "200",
            cls.headers(),
            {
                "env_id": fake_id("env"),
                "done": False,
                "task": "StarCraftMining-v0",
                "reward": 0.52,
                "observation": StarCraftImageFileTest.test_image().to_b64_screen_buffer()
            })

    @classmethod
    def reset_env_response(cls):
        return (
            "200",
            cls.headers(),
            {
                "env_id": fake_id("env"),
                "task": "StarCraftMining-v0",
                "observation": StarCraftImageFileTest.test_image().to_b64_screen_buffer()
            })

    @classmethod
    def close_env_response(cls):
        return (
            "200",
            cls.headers(),
            {
                "env_id": fake_id("env"),
            })
