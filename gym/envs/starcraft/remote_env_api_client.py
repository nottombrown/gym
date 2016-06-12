from gym.envs.starcraft import remote_env_api_requestor

class StarCraftClientException(Exception):
    def __init__(self, msg, response):
        super(Exception, msg)
        self.response = response


class NoAvailableWorkersException(StarCraftClientException):
    pass


class OutOfSyncAPIException(StarCraftClientException):
    pass


class RemoteEnvAPIClient(object):
    """
    Stateless client for the StarCraftAPI
    """
    def request(self, endpoint, headers, body):
        # This is verbose, but it makes it easier to patch in RemoteEnvAPITestCase
        return remote_env_api_requestor.RemoteEnvAPIRequestor.request(endpoint, headers, body)

    def create_env(self):
        _, _, body = self.request("POST v1/envs", {}, {})
        return body

    def step_env(self, env_id, mouse_keyboard_action):
        """Makes an action from a payload and returns a dump of the screen"""
        _, _, body = self.request("POST v1/envs/{0}/step".format(env_id), {}, mouse_keyboard_action)
        return body

    def reset_env(self, env_id, data):
        _, _, body = self.request("POST v1/envs/{0}/reset".format(env_id), {}, data)
        return body

    def close_env(self, env_id):
        _, _, body = self.request("POST v1/envs/{0}/close".format(env_id), {}, {})
        return body