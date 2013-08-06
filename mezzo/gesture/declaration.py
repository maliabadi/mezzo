from mezzo.gesture import Gesture

class Declaration(Gesture):
    """
    Format:
        { "namespace":
            { "some object": { "attribute name" : "value" } } }
    """
    require = ['namespace', 'state']

    def __init__(self, **kwargs):
        super(Declaration, self).__init__('declaration', **kwargs)

    def run(self):
        self.validate()
        self.state.setNameSpace(self.namespace)
