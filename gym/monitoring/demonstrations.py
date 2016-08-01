import base64
from io import BytesIO

import numpy as np
import pickle


class DemonstrationRecorder(object):
    def __init__(self, file_name):
        self.file = open(file_name, 'w')

    def record_step(self, action, observation):

        # Write Action (1 line)
        self.file.write(str(action))
        self.file.write("\n")

        # Write Observation (1 line)
        obs_string = base64.b64encode(observation.tostring())
        self.file.write(obs_string)
        self.file.write("\n")

    def close(self):
        self.file.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class DemonstrationReader(object):
    def __init__(self, file_name, obs_dtype="uint8", obs_shape=(210, 160, 3)):
        self.file = open(file_name, 'rb')
        self.obs_dtype = obs_dtype
        self.obs_shape = obs_shape

    def __iter__(self):
        return self

    def next(self):
        action_string = self.file.readline()
        if action_string == "":
            raise StopIteration()

        action = int(action_string)

        observation_string = self.file.readline()
        observation_string = base64.b64decode(observation_string)

        observation = np.fromstring(observation_string, dtype=self.obs_dtype).reshape(self.obs_shape)
        return action, observation


if __name__ == '__main__':
    import gym
    from gym.monitoring.demonstrations import DemonstrationReader

    recorder = DemonstrationRecorder("/tmp/pong.demo")
    obs = np.arange(10)
    recorder.record_step(1, obs)
    recorder.close()

    reader = DemonstrationReader("/tmp/pong.demo", obs_dtype='int64', obs_shape=(10,))
    for action, observation in reader:
        print(action)
        print(observation)
