import zmq
import json
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


class StarCraftAPIClient(object):
    """
    Stateless client for the StarCraftAPI
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

        # TODO: remove this fixed_obs
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
        # TODO: Find a place to handle errors
        # TODO: Find a place to set headers
        # TODO: How should we address security - certs etc.

        print("POST %s ..." % endpoint)

        request = (
            "POST " + endpoint,
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

    def create_env(self):
        _, _, body = self._post("v1/envs", {}, {})
        return body

    def step_env(self, env_id, mouse_keyboard_action):
        """Makes an action from a payload and returns a dump of the screen"""
        _, _, body = self._post("v1/envs/{0}/step".format(env_id), {}, mouse_keyboard_action)
        return body

    def close_env(self, env_id):
        _, _, body = self._post("v1/envs/{0}/close".format(env_id), {}, {})
        return body

    def reset_env(self, env_id, data):
        _, _, body = self._post("v1/envs/{0}/reset".format(env_id), {}, data)
        return body
