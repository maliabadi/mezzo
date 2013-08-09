import json
from pprint import pprint

from mezzo.state import MezzoState
from mezzo.gesture import *


def deserialize(data):
    return MezzoProgram(**json.loads(data))


def deserializeGesture(gesture):
    return key_to_class[gesture.pop('type')](**gesture)


class MezzoProgram(object):

    def __init__(self, objects={}, directives=[], **kwargs):
        self.state = MezzoState(objects)
        self.directives = map(lambda x: deserializeGesture(x),
                              directives)
        for gesture in self.directives:
            gesture.bindTo(self.state)

    def run(self):
        for gesture in self.directives:
            gesture.run()
