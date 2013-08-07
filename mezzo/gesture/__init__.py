from mezzo.state import MezzoState


gestures = ['declaration', 'alteration', 'iteration',
            'recursion', 'flow', 'comparison',
            'binding', 'invocation', 'block']


class Gesture(object):
    """
    Base Gesture class and the list of supported gesture types
    """

    require = []

    def __init__(self, kind, **kwargs):
        if not kind in gestures:
            raise ValueError("Gesture Type '%s' not supported" % kind)
        self.kind = kind
        for key, value in kwargs.items():
            setattr(self, key, value)

    def bindTo(self, state):
        if not isinstance(state, MezzoState):
            raise ValueError("Cannot bind gesture non-MezzoState object")
        self.state = state

    def validate(self):
        for name in self.require:
            if not hasattr(self, name):
                raise ValueError

    def serialize(self):
        struct = {'type': self.kind}
        for name in self.require:
            if name != 'state':
                struct[name] = getattr(self, name)
        return struct
