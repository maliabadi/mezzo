from mezzo.gesture import Gesture

class Flow(Gesture):
    """
    Format: 
        { "chain": [
        { "if": { "type": "comparison", "chain" : []},
          "do": [ { "type" : "gesture", "body" : "..." } ],
          "break": 1 } ] }
    """

    require = ['chain', 'state']

    def __init__(self, **kwargs):
        super(Flow, self).__init__('flow', **kwargs)

    def run(self):
        self.validate()
        #TODO
