#!/usr/bin/env python
import sys, gym, logging, time
from gym.envs.starcraft.mouse_keyboard_action import MouseKeyboardAction


class MouseKeyboardAgent(object):
    """
    MouseAgent listens to the viewer to see if there has been any human input since the last
    call to `act()`. If so, it returns an action, if not, it returns the null action
    """
    def __init__(self, action_space):
        self.action_space = action_space
        self._next_action = MouseKeyboardAction.null()

        env.render() # TODO: Remove this and see if things still work
        env.viewer.window.on_key_press = self.key_press
        env.viewer.window.on_key_release = self.key_release
        env.viewer.window.on_mouse_press = self.mouse_press
        env.viewer.window.on_mouse_release = self.mouse_release

    def act(self, observation, reward, done):
        """ Do the action and reset the next_action"""
        mouse_keyboard_action = self._next_action
        self._next_action = MouseKeyboardAction.null()
        return mouse_keyboard_action.to_np()

    def key_press(self, key, modifiers):
        self._next_action = MouseKeyboardAction.from_key_event(key, modifiers)

    def key_release(self, key, modifiers):
        self._next_action = MouseKeyboardAction.from_key_event(key, modifiers)

    def mouse_press(self, x, y, button, modifiers):
        print("Mouse pressed: " + str((x, y)))
        self._next_action = MouseKeyboardAction.from_mouse_event(x, y, button, modifiers)

    def mouse_release(self, x, y, button, modifiers):
        print("Mouse released: " + str((x, y)))
        self._next_action = MouseKeyboardAction.from_mouse_event(x, y, button, modifiers)

if __name__ == '__main__':
    # You can optionally set up the logger. Also fine to set the level
    # to logging.DEBUG or logging.WARN if you want to change the
    # amount of output.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    env = gym.make('StarCraftBasic-v0' if len(sys.argv)<2 else sys.argv[1])
    agent = MouseKeyboardAgent(env.action_space)

    episode_count = 10
    max_steps = 20000
    reward = 0
    done = False

    for i in range(episode_count):
        ob = env.reset()

        for j in range(max_steps):
            env.render()

            action = agent.act(ob, reward, done)
            ob, reward, done, _ = env.step(action)
            if done:
                break

            time.sleep(1.0/30) # Render at 30 fps