from mezzo.gesture import Gesture
from mezzo.state import *
from mezzo.gesture.alteration import Alteration
from mezzo.gesture.binding import Binding

# temporary
key_to_class = {'alteration': Alteration}


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
        self.loadreferences()
        self.iterargs(mode='write')
        self.asdot[dotform(self.mp.objectChain())] = {self.mp.value(): 'body'}
        body = self.state.getNameSpace(self.asdot)
        for gest in body:
            gestureObject = key_to_class[gest.pop('type')](**gest)
            gestureObject.bindTo(self.state)
            gestureObject.run()
        self.iterargs(mode='clear')

    def loadreferences(self):
        self.mp = MezzoPath(self.namespace)
        self.asdot = dotdict(self.namespace)

    def iterargs(self, mode='write'):
        for k, v in self.arguments.items():
            send = v if mode == 'write' else False
            tail = {self.mp.value(): {'arguments': k}}
            self.asdot[dotform(self.mp.objectChain())] = tail
            self.state.setNameSpace(read_form_to_write(self.asdot, send))


if __name__ == "__main__":
    state = MezzoState({'foo': {'varone': 0, 'baz': {'bar': 0}, 'adder': 1}})
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
                 'varone': 0,
                 'baz': {'bar': 0},
                 'adder': 1}}
    assert state.namespaces == a
    invocation = Invocation(namespace={'foo': 'myfunction'},
                            arguments={'argone': 2, 'argtwo': 2})
    invocation.bindTo(state)
    invocation.run()
    b = {'foo': {'myfunction': {'body': [{'right': {'foo': 'adder'},
                                          'type': 'alteration',
                                          'center': 'pluseq',
                                          'left': {'foo': {'baz': 'bar'}}}],
                                'arguments': {'argtwo': False,
                                              'argone': False},
                                'locals': {'localtwo': False,
                                           'localone': False}},
                 'varone': 0,
                 'baz': {'bar': 1},
                 'adder': 1}}
    print state.namespaces
