import unittest
from gym.envs.starcraft.starcraft_api_client import StarCraftAPIClient
from gym.envs.starcraft.tests.helper import StarCraftAPITestCase, TestData


class StarCraftAPIClientTest(StarCraftAPITestCase):

    def setUp(self):
        self.game_client = StarCraftAPIClient()

    def test_create_env(self):
        self.game_client
