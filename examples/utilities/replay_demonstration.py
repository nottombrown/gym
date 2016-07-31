from time import sleep

from gym.monitoring.demonstrations import DemonstrationReader
from gym.envs.classic_control import rendering

if __name__ == '__main__':

    reader = DemonstrationReader('/tmp/atari.demo')

    for action, observation in reader:
        viewer = rendering.SimpleImageViewer()
        viewer.imshow(observation)
        sleep(0.01)