import zmq
import json
from PIL import Image

from gym.envs.starcraft.starcraft_image_plugin import StarCraftImageFile
import numpy as np

class StarCraftClientException(Exception):
    def __init__(self, msg, response):
        super(Exception, msg)
        self.response = response


class NoAvailableWorkersException(StarCraftClientException):
    pass

class OutOfSyncAPIException(StarCraftClientException):
    pass

class RemoteStarCraftGameClient(object):
    """
    Thin client around the StarCraftGameAPI
    """

    def __init__(self):

        context = zmq.Context()

        # Store the last observed state
        self._state = None

        #  Socket to talk to server
        print("Connecting to StarCraftServer...")
        self.socket = context.socket(zmq.REQ)
        self.episode_id = None

        windows_server_2012_url = "tcp://0.tcp.ngrok.io:19085"
        self.socket.connect(windows_server_2012_url)

    def _post(self, endpoint, headers, body):
        """
        Parameters
        ----------
        endpoint
        headers
        body

        Returns
        -------
        status
        headers
        body
        """

        # print("Sending command %s ..." % command)
        #
        # request = {
        #     "command": command,
        #     "data": data
        # }
        # self.socket.send_json(request)
        #
        # response = json.loads(self.socket.recv())
        # print("Received state from server")
        #
        # return response

        # Hack to get an image
        # img = Image.open("/tmp/starcraft_screenshot.scif")

        body = {
            "done": False,
            "observation": np.array(bytearray([])),
            "reward": 1.0
        }

        return (
            "200",
            {},
            body
        )

    def step(self, mouse_keyboard_action):
        """Makes an action from a payload and returns a dump of the screen"""
        _, _, body = self._post("v1/envs/env_id/step", {}, mouse_keyboard_action)
        return body["observation"], body["reward"], body["done"], {}

    def close(self):
        return self._post("v1/envs/env_id/close", {}, {})

    def reset(self):
        # TODO: Throw an error if we already episode_id set
        data = {
            "map": "StarCraftMining-v0",
        }
        _, _, body = self._post("v1/envs/env_id/reset", {}, data)
        return body["observation"], body["reward"], body["done"], {}

