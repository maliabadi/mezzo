from mezzo.gesture import Gesture


class Binding(Gesture):
    """
    Format:
        { "namespace": {"an object": {"a nested object": "attribute name"}},
          "arguments": { "a named argument" : "default value",
                         "a named argument" : "default value" },
          "locals" : [ "attribute name", "attibute name", "attribute name"],
          "directives" : [ { "type" : "gesture", "body": "..." } ] }
    """

    require = ['namespace', 'arguments', 'locals', 'directives']

    def __init__(self, **kwargs):
        super(Binding, self).__init__('compare', **kwargs)

    def run(self):
        self.validate()
        #TODO
