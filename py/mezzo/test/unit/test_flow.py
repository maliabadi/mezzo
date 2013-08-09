import unittest

from mezzo.state import MezzoState
from mezzo.gesture import Compare, Alteration, Flow


class FlowTest(unittest.TestCase):

    def runTest(self):
        state = MezzoState({'foo': {'a': 0,
                                    'b': 1,
                                    'c': 2,
                                    'd': 0,
                                    'baz': {'bar': 0},
                                    'adder': 1}})
        comparison = Compare(chain=[{"left": {"foo": "a"},
                                     "center": "eq",
                                     "right": {"foo": "d"}},
                                    {"continue": "and"},
                                    {"left": {'foo': 'c'},
                                     "center": "gt",
                                     "right": {'foo': 'b'}}])
        alteration = Alteration(left={'foo': {'baz': 'bar'}},
                                center="pluseq",
                                right={'foo': 'adder'})
        flowchain = [{'comparison': comparison,
                      'do': [alteration],
                      'stop': False}]
        flow = Flow(chain=flowchain)
        comparison.bindTo(state)
        alteration.bindTo(state)
        flow.bindTo(state)
        flow.run()
        self.assertEqual(state.namespaces, {'foo': {'a': 0,
                                            'c': 2,
                                            'b': 1,
                                            'd': 0,
                                            'baz': {'bar': 1},
                                            'adder': 1}})


if __name__ == "__main__":
    unittest.main()
