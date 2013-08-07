import unittest

from mezzo.state import MezzoState
from mezzo.gesture import Binding


class BindingTest(unittest.TestCase):

    def runTest(self):
        state = MezzoState({'foo': {'varone': 0}})
        function = Binding(namespace={'foo': 'myfunction'},
                           arguments={'argone': 1, 'argtwo': 2},
                           locals=['localone', 'localtwo'],
                           body=[{'type': 'alteration',
                                  'left': {'foo': {'baz': 'bar'}},
                                  'center': 'pluseq',
                                  "right": {'foo': 'adder'}}])
        function.bindTo(state)
        function.run()
        a = {'foo': {'myfunction': {'body': [{'right': {'foo': 'adder'},
                                              'type': 'alteration',
                                              'center': 'pluseq',
                                              'left': {'foo':
                                                       {'baz': 'bar'}}}],
                                    'arguments': {'argtwo': 2,
                                                  'argone': 1},
                                    'locals': {'localtwo': False,
                                               'localone': False}},
                     'varone': 0}}
        self.assertEqual(state.namespaces, a)


if __name__ == "__main__":
    unittest.main()
