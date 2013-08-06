from mezzo.gesture import Gesture

class Compare(Gesture):
    """
    Format: 
        { "chain": [ { "left": {"an object": {"a nested object": "attribute name"}}, 
                       "center": "eq",
                       "right": {"an object": {"a nested object": "attribute name"}}, 
                       "negate": "false" },
                     { "continue": "and" },
                     { "left": {"an object": {"a nested object": "attribute name"}}, 
                       "center": "lt",
                       "right": {"an object": {"a nested object": "attribute name"}}, 
                       "negate": "false" } ] }
    """

    require = ['chain', 'state']

    def __init__(self, **kwargs):
        super(Compare, self).__init__('compare', **kwargs)

    def run(self):
        self.validate()
        #TODO
