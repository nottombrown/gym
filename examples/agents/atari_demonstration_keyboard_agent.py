#!/usr/bin/env python
from __future__ import print_function

import gym
import sys
import time

#
# Test yourself as a learning agent! Pass environment name as a command-line argument.
#

env = gym.make('Pong-v0' if len(sys.argv)<2 else sys.argv[1])

ACTIONS = env.action_space.n
ROLLOUT_TIME = 1000
SKIP_CONTROL = 0    # Use previous control decision SKIP_CONTROL times, that's how you
                    # can test what skip is still usable.

human_agent_action = 0
human_wants_restart = False
human_sets_pause = False

def key_press(key, mod):
    global human_agent_action, human_wants_restart, human_sets_pause
    print("Pressed: {}".format(key))

    if key==0xff0d: human_wants_restart = True
    if key==32: human_sets_pause = not human_sets_pause

    if key == 65362: # up arrow
        key = 50
    if key == 65364: # down arrow
        key = 51

    a = key - ord('0')
    if a <= 0 or a >= ACTIONS: return
    human_agent_action = a

def key_release(key, mod):
    print("Released: {}".format(key))
    global human_agent_action
    human_agent_action = 0

env.render()
env.viewer.window.on_key_press = key_press
env.viewer.window.on_key_release = key_release

def rollout(env):
    global human_agent_action, human_wants_restart, human_sets_pause
    human_wants_restart = False
    obser = env.reset()
    for t in range(ROLLOUT_TIME):

        a = human_agent_action
        print("Action: {}".format(a))

        obser, r, done, info = env.step(a)

        env.render()

        # Slow down the game to make it easier for me to play
        time.sleep(0.08)

        if done: break
        if human_wants_restart: break
        while human_sets_pause:
            env.render()
            time.sleep(0.1)

print("ACTIONS={}".format(ACTIONS))
print("Press keys 1 2 3 ... to take actions 1 2 3 ...")
print("No keys pressed is taking action 0")

while 1:
    rollout(env)
