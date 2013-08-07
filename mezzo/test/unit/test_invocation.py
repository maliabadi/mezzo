import unittest

from mezzo.state import MezzoState
from mezzo.gesture import Alteration, Binding, Invocation


class InvocationTestOne(unittest.TestCase):

    def runTest(self):
        state = MezzoState({'foo': {'varone': 0,
                            'baz': {'bar': 0},
                            'adder': 1}})
        alteration = Alteration(left={'foo': {'baz': 'bar'}},
                                center="pluseq",
                                right={'foo': 'adder'})
        function = Binding(namespace={'foo': 'myfunction'},
                           arguments={'argone': 1, 'argtwo': 2},
                           locals=['localone', 'localtwo'],
                           body=[{'type': 'alteration',
                                  'left': {'foo': {'baz': 'bar'}},
                                  'center': 'pluseq',
                                  'right': {'foo': 'adder'}}])
        invocation = Invocation(namespace={'foo': 'myfunction'},
                                arguments={'argone': 2, 'argtwo': 2})
        function.bindTo(state)
        invocation.bindTo(state)
        function.run()
        invocation.run()
        tar = {'foo': {'adder': 1,
               'baz': {'bar': 1},
               'myfunction': {'arguments': {'argone': False, 'argtwo': False},
                              'body': [{'center': 'pluseq',
                                        'left': {'foo': {'baz': 'bar'}},
                                        'right': {'foo': 'adder'}}],
                              'locals': {'localone': False,
                                         'localtwo': False}},
               'varone': 0}}
        self.assertEqual(state.namespaces, tar)


if __name__ == "__main__":
    unittest.main()
