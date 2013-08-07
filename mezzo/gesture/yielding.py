from mezzo.gesture import Gesture


class Yielding(Gesture):
    """
    Format:
        {"open": [ { "type" : "gesture", "body": "..." } ],
        "close": [ { "type" : "gesture", "body": "..." } ],
        "body": [ { "type" : "gesture", "body": "..." } ],
        "except" : "die" }
    """

    require = ['open', 'close', 'body', 'except']

    def __init__(self, **kwargs):
        super(Yielding, self).__init__('yielding', **kwargs)

    def run(self):
        self.validate()
        #TODO
