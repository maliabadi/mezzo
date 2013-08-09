import unittest

from mezzo.state import MezzoState
from mezzo.gesture import Alteration


class AlterationTest(unittest.TestCase):

    def runTest(self):
        state = MezzoState({'foo': {'baz': {'bar': 0}, 'adder': 4}})
        alteration = Alteration(left={'foo': {'baz': 'bar'}},
                                center="pluseq",
                                right={'foo': 'adder'})
        alteration.bindTo(state)
        alteration.run()
        self.assertEqual(state.namespaces, {'foo': {'baz': {'bar': 4},
                                            'adder': 4}})


if __name__ == "__main__":
    unittest.main()
