import unittest
from gym.envs.starcraft.remote_starcraft_game_client import RemoteStarCraftGameClient
from gym.envs.starcraft.tests.helper import StarCraftAPITestCase, TestData


class RemoteStarCraftGameClientTest(StarCraftAPITestCase):

    def setUp(self):
        self.game_client = RemoteStarCraftGameClient()

    def test_create_env(self):
        self.game_client
