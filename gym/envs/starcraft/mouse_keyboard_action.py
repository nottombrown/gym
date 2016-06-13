import numpy as np


class MouseKeyboardAction(object):
    """
    Represents a mouse or keyboard event. Follows the event types from the VNC RFB Protocol
    https://www.realvnc.com/docs/rfbproto.pdf

    It will contain one of the following events:
        KeyEvent
        PointerEvent
    """
    def __init__(self, x, y, button, key, modifiers):
        self.x = x
        self.y = y
        self.button = button
        self.key = key
        self.modifiers = modifiers

    @classmethod
    def null(cls):
        return cls(0, 0, 0, 0, 0)

    @classmethod
    def from_mouse_event(cls, x, y, button, modifiers):
        return cls(x, y, button, 0,  modifiers)

    @classmethod
    def from_key_event(cls, key, modifiers):
        return cls(0, 0, 0, key,  modifiers)

    @classmethod
    def from_np(cls, np_array):
        return cls(*np_array.tolist())

    def to_np(self):
        return np.array([self.x, self.y, self.button, self.key, self.modifiers])

    def to_dict(self):
        return {
            "mouse": {
                "x": self.x,
                "y": self.y,
                "button": self.button
            },
            "key": self.key,
            "modifiers": self.modifiers
        }
