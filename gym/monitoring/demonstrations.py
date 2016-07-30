from io import BytesIO

import numpy as np
import pickle

class DemonstrationRecorder(object):
    def __init__(self, fn):
        self.file = open(fn, 'w')

    def record_step(self, action, observation):

        # pair = (action, observation)
        # pickle.dump(pair, self.file)


        # Write Action (1 line)
        # self.file.write(str(action))
        # self.file.write("\n")

        np.save(self.file, observation)
        # np.save(self.file, observation)

        #
        # # Write Observation (2 lines)
        # obs_stream = StringIO.StringIO()
        # np.save(obs_stream, observation)
        # self.file.write(obs_stream.getvalue())
        # self.file.write("\n")

    def close(self):
        self.file.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class DemonstrationReader(object):
    def __init__(self, fn):
        self.file = open(fn, 'rb')

    def __iter__(self):
        return self

    def next(self):
        # action = self.file.readline()

        # Use this: http://stackoverflow.com/questions/25837641/save-retrieve-numpy-array-from-string

        # Read 2 lines
        obs_stream = BytesIO()
        obs_stream.write(self.file.read())
        # obs_stream.write(self.file.readline())
        #
        # value = obs_stream.getvalue()
        # print(value)
        data = self.file.read()

        # observation = np.load(self.file)
        observation = np.load(obs_stream)
        return observation
        # return action, observation


if __name__ == '__main__':

    import gym
    from gym.monitoring.demonstrations import DemonstrationReader


    recorder = DemonstrationRecorder("/tmp/pong.demo")
    recorder.record_step(1, np.arange(10))
    recorder.close()

    reader = DemonstrationReader("/tmp/pong.demo")
    print(reader.next())
