#!/usr/bin/env python
import sys, gym

#
# Test yourself as a learning agent! Pass environment name as a command-line argument.

env = gym.make('StarCraftBasic-v0' if len(sys.argv)<2 else sys.argv[1])

ACTIONS = env.action_space.n
ROLLOUT_TIME = 1000

human_agent_action = 0
human_wants_restart = False
human_sets_pause = False

def key_press(key, mod):
    global human_agent_action, human_wants_restart, human_sets_pause
    if key==0xff0d: human_wants_restart = True
    if key==32: human_sets_pause = not human_sets_pause
    a = key - ord('0')
    if a <= 0 or a >= ACTIONS: return
    human_agent_action = a

def key_release(key, mod):
    global human_agent_action
    a = key - ord('0')
    if a <= 0 or a >= ACTIONS: return
    if human_agent_action == a:
        human_agent_action = 0

def mouse_press(x, y, button, modifiers):
    print "Mouse pressed: " + str((x, y))
    _make_mouse_action(x, y, button, modifiers)

def mouse_release(x, y, button, modifiers):
    print "Mouse released: " + str((x, y))
    _make_mouse_action(x, y, button, modifiers)


def _make_mouse_action(x, y, button, modifiers):
    global human_agent_action
    action_payload = {
        "command": "make_action",
        "mouse": {
            "x": x,
            "y": y,
            "button": button
        },
        "modifiers": modifiers
    }
    # TODO: Encode this into action_space
    human_agent_action = action_payload


env.render()
env.viewer.window.on_key_press = key_press
env.viewer.window.on_key_release = key_release
env.viewer.window.on_mouse_press = mouse_press
env.viewer.window.on_mouse_release = mouse_release

def rollout(env):
    global human_agent_action, human_wants_restart, human_sets_pause
    human_wants_restart = False
    obser = env.reset()
    skip = 0
    for t in xrange(ROLLOUT_TIME):
        env.render()

        # We can only advance the game on user actions, by moving this to the on_X functions
        obser, r, done, info = env.step(human_agent_action)
        if done: break

        # Only do the human_agent_action once
        human_agent_action = 0

        if human_wants_restart: break
        while human_sets_pause:
            env.render()
            import time
            time.sleep(0.1)

print "ACTIONS={}".format(ACTIONS)
print "Press keys 1 2 3 ... to take actions 1 2 3 ..."
print "No keys pressed is taking action 0"

while 1:
    rollout(env)
