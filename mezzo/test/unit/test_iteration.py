import unittest

from mezzo.state import MezzoState
from mezzo.gesture import Alteration, Iteration


class IterationTest(unittest.TestCase):

    def runTest(self):
        state = MezzoState({'foo': {'baz': {'bar': [1, 2, 3]},
                                    'counter': 0,
                                    'adder': 3}})
        each = {'foo': {'baz': 'bar'}}
        local = {'foo': 'index'}
        alteration = Alteration(left={'foo': 'counter'},
                                center="pluseq",
                                right={'foo': 'adder'})
        iteration = Iteration(each=each,
                              local=local,
                              do=[alteration])
        alteration.bindTo(state)
        iteration.bindTo(state)
        iteration.run()
        self.assertEqual(state.namespaces, {'foo': {'counter': 9,
                                            'baz': {'bar': [1, 2, 3]},
                                            'adder': 3}})


if __name__ == "__main__":
    unittest.main()
