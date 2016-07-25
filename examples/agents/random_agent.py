import argparse
import logging
import os, sys

import gym

class RandomAgent(object):
    """
    The world's simplest agent!

    Example usage

        python examples/agents/random_agent.py -e CartPole-v0
        python examples/agents/random_agent.py -e SpaceInvaders-v0 -b bmrun_XhApLPUiSoyj2TpGpotuSQ

    """
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()

if __name__ == '__main__':
    # You can optionally set up the logger. Also fine to set the level
    # to logging.DEBUG or logging.WARN if you want to change the
    # amount of output.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('-e', '--environment', default='CartPole-v0', help='Which environment to run on.')
    parser.add_argument('-b', '--benchmark_run_id', default=None, help='Which benchmark run this is associated with.')
    args = parser.parse_args()

    # atari_envs = ['AirRaid-v0', 'Alien-v0', 'Amidar-v0', 'Assault-v0', 'Asterix-v0', 'Asteroids-v0', 'Atlantis-v0',
    #               'BankHeist-v0', 'BattleZone-v0', 'BeamRider-v0', 'Berzerk-v0', 'Bowling-v0', 'Boxing-v0',
    #               'Breakout-v0', 'Carnival-v0', 'Centipede-v0', 'ChopperCommand-v0', 'CrazyClimber-v0',
    atari_envs = ['DemonAttack-v0', 'DoubleDunk-v0', 'ElevatorAction-v0', 'Enduro-v0', 'FishingDerby-v0', 'Freeway-v0',
                  'Frostbite-v0', 'Gopher-v0', 'Gravitar-v0', 'IceHockey-v0', 'Jamesbond-v0', 'JourneyEscape-v0',
                  'Kangaroo-v0', 'Krull-v0', 'KungFuMaster-v0', 'MontezumaRevenge-v0', 'MsPacman-v0', 'NameThisGame-v0',
                  'Phoenix-v0', 'Pitfall-v0', 'Pong-v0', 'Pooyan-v0', 'PrivateEye-v0', 'Qbert-v0', 'Riverraid-v0',
                  'RoadRunner-v0', 'Robotank-v0', 'Seaquest-v0', 'Skiing-v0', 'Solaris-v0', 'SpaceInvaders-v0',
                  'StarGunner-v0', 'Tennis-v0', 'TimePilot-v0', 'Tutankham-v0', 'UpNDown-v0', 'Venture-v0',
                  'VideoPinball-v0', 'WizardOfWor-v0', 'YarsRevenge-v0', 'Zaxxon-v0']


    for environment in atari_envs:
        env = gym.make(environment)

        # You provide the directory to write to (can be an existing
        # directory, including one with existing data -- all monitor files
        # will be namespaced). You can also dump to a tempdir if you'd
        # like: tempfile.mkdtemp().
        outdir = '/tmp/random-agent-results'
        env.monitor.start(outdir, force=True, seed=0)

        # This declaration must go *after* the monitor call, since the
        # monitor's seeding creates a new action_space instance with the
        # appropriate pseudorandom number generator.
        agent = RandomAgent(env.action_space)

        episode_count = 100
        max_steps = 200
        reward = 0
        done = False

        for i in range(episode_count):
            ob = env.reset()

            for j in range(max_steps):
                action = agent.act(ob, reward, done)
                ob, reward, done, _ = env.step(action)
                if done:
                    break
                # Note there's no env.render() here. But the environment still can open window and
                # render if asked by env.monitor: it calls env.render('rgb_array') to record video.
                # Video is not recorded every episode, see capped_cubic_video_schedule for details.

        # Dump result info to disk
        env.monitor.close()

        # Upload to the scoreboard. We could also do this from another
        # process if we wanted.
        logger.info("Successfully ran RandomAgent. Now trying to upload results to the scoreboard. If it breaks, you can always just try re-uploading the same results.")
        gym.upload(outdir, benchmark_run_id=args.benchmark_run_id)
