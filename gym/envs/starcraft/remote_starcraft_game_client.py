import zmq
import json
from base64 import b64decode
import numpy as np
from PIL import Image

from gym.envs.starcraft.starcraft_image_file import StarCraftImageFile

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

        img = Image.open('/tmp/starcraft_screenshot.scif')
        img.to_np_rgb()

        new_img = StarCraftImageFile.from_np_array(img.to_obs())
        new_img.to_np_rgb()


        self._fixed_obs = img.to_obs()


    def _post(self, endpoint, headers, body):
        """
        Args:
            (endpoint, headers, body)

        Returns:
            (status, headers, body)
        """

        print("POST %s ..." % endpoint)

        request = (
            endpoint,
            json.dumps(headers),
            json.dumps(body),
        )
        self.socket.send_multipart(request)

        status, response_headers, response_body = self.socket.recv_multipart(request)
        print("Response %s" % status)

        return (
            status,
            json.loads(response_headers),
            json.loads(body)
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

