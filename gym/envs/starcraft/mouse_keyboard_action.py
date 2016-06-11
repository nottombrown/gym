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
        #TODO: store this internally
        pass

    @classmethod
    def from_np(cls, np_action_vector):
        return cls(np.array([0,0,0,0]))

    @classmethod
    def from_mouse_event(cls, x, y, button, modifiers):
        return cls(np.array([0, 0, 0, 0]))

    @classmethod
    def from_key_event(cls, key, modifiers):
        return cls()

    @classmethod
    def from_json(cls, np_action_vector):
        return cls()

    @classmethod
    def null(cls):
        return cls(0, 0, 0, 0)


    def to_np(self):
        return np.array([0, 0, 0, 0])

    def to_json(self):
        """
        Example JSON:

        {
            "mouse": {
                "x": 319,
                "y": 211,
                "button": 1
            },
            "key": 19
            "modifiers": 2
        }
        """

