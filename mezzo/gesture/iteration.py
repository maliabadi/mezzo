from mezzo.gesture import Gesture

class Iteration(Gesture):
    """
    Format: 
        { "each" : {"an object": {"a nested object": "attribute name for an iterable feature"}},
          "local" : {"iterable locals": "attribute name for an iterable feature"},
          "do" : [ { "type" : "gesture", "body" : "..." } ]
        }
    """

    require = ['each', 'local', 'do']

    def __init__(self, **kwargs):
        super(Iteration, self).__init__('iteration', **kwargs)

    def run(self):
        self.validate()
        #TODO
