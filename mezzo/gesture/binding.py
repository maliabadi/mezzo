from mezzo.gesture import Gesture
from mezzo.state import *
from mezzo.gesture.alteration import Alteration


class Binding(Gesture):
    """
    Format:
        { "namespace": {"an object": {"a nested object": "attribute name"}},
          "arguments": { "a named argument" : "default value",
                         "a named argument" : "default value" },
          "locals" : [ "attribute name", "attibute name", "attribute name"],
          "body" : [ { "type" : "gesture", "body": "..." } ] }
    """

    require = ['namespace', 'arguments', 'locals', 'body', 'state']

    def __init__(self, **kwargs):
        super(Binding, self).__init__('binding', **kwargs)

    def run(self):
        self.validate()
        self.loadReferences()
        self.register()

    def register(self):
        self.registerArguments()
        self.registerLocals()
        self.registerBody()

    def loadReferences(self):
        self.asdot = dotdict(self.namespace)
        self.mp = MezzoPath(self.asdot)
        self.objchain = dotform(self.mp.objectChain())

    def registerArguments(self):
        for key, value in self.arguments.items():
            self.asdot[self.objchain] = {self.mp.value(): {'arguments': key}}
            self.state.setNameSpace(read_form_to_write(self.asdot, value))

    def registerLocals(self):
        for name in self.locals:
            self.asdot[self.objchain] = {self.mp.value(): {'locals': name}}
            self.state.setNameSpace(read_form_to_write(self.asdot, False))

    def registerBody(self):
        self.asdot[self.objchain] = {self.mp.value(): 'body'}
        gestures = [x.serialize() for x in self.body]
        self.state.setNameSpace(read_form_to_write(self.asdot, gestures))


if __name__ == "__main__":
    state = MezzoState({'foo': {'varone': 0}})
    alteration = Alteration(left={'foo': {'baz': 'bar'}},
                            center="pluseq",
                            right={'foo': 'adder'})
    function = Binding(namespace={'foo': 'myfunction'},
                       arguments={'argone': 1, 'argtwo': 2},
                       locals=['localone', 'localtwo'],
                       body=[alteration])
    function.bindTo(state)
    function.run()
    a = {'foo': {'myfunction': {'body': [{'right': {'foo': 'adder'},
                                          'type': 'alteration',
                                          'center': 'pluseq',
                                          'left': {'foo': {'baz': 'bar'}}}],
                                'arguments': {'argtwo': 2,
                                              'argone': 1},
                                'locals': {'localtwo': False,
                                           'localone': False}},
                 'varone': 0}}
    assert state.namespaces == a
