from mezzo.gesture import Gesture

class Recursion(Gesture):
    """
    Format: 
        { "break": { "type": "comparison", "chain" : [] },
          "do": [ { "type" : "gesture", "body": "..." } ] }
    """

    require = ['break', 'do', 'state']

    def __init__(self, **kwargs):
        super(Recursion, self).__init__('recursion', **kwargs)

    def run(self):
        self.validate()
        #TODO
