from mezzo.gesture import Gesture

class Invocation(Gesture):
    """
    Format: 
        { "namespace": {"an object": {"a nested object": "attribute name"}},
          "arguments": { "named argument" : { "some": "namespace path" },
                         "a named argument": { "some": "namespace path" }}}
    """

    require = ['namespace', 'arguments']

    def __init__(self, **kwargs):
        super(Invocation, self).__init__('invocation', **kwargs)

    def run(self):
        self.validate()
        #TODO
