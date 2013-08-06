from mezzo.gesture import Gesture

class Alteration(Gesture):
    """
    Format: 
        {"left" : { "some object": "attribute name"},
         "center" : "andeq", 
         "right" : 1 }
    """

    require = ['left', 'center', 'right' 'state']

    def __init__(self, **kwargs):
        super(Alteration, self).__init__('alteration', **kwargs)

    def run(self):
        self.validate()
        #TODO
