from gym.envs.starcraft import remote_env_api_requestor


class RemoteEnvAPIClient(object):
    """
    Stateless client for the StarCraftAPI
    """
    def request(self, endpoint, headers, body):

        # This is verbose, but it makes it easier to patch in RemoteEnvAPITestCase
        (status, headers, body) = remote_env_api_requestor.RemoteEnvAPIRequestor.request(endpoint, headers, body)

        # TODO: Add error-handling and header-checking here
        return status, headers, body

    # TODO: Validate params in these API methods
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


class RemoteEnvAPIClientException(Exception):
    def __init__(self, msg, response):
        super(Exception, msg)
        self.response = response


class NoAvailableWorkersException(RemoteEnvAPIClientException):
    pass


class OutOfSyncAPIException(RemoteEnvAPIClientException):
    pass
