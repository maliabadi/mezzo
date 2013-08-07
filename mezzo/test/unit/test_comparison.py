import unittest

from mezzo.state import MezzoState
from mezzo.gesture import Compare


class ComparisonTestTrue(unittest.TestCase):

    def runTest(self):
        state = MezzoState({'foo': {'a': 0, 'b': 1, 'c': 2, 'd': 0}})
        chain = [{"left": {"foo": "a"},
                  "center": "eq",
                  "right": {"foo": "d"}},
                 {"continue": "and"},
                 {"left": {'foo': 'c'},
                  "center": "gt",
                  "right": {'foo': 'b'}}]
        comp = Compare(chain=chain)
        comp.bindTo(state)
        self.assertTrue(comp.run())


class ComparisonTestFalse(unittest.TestCase):

    def runTest(self):
        state = MezzoState({'foo': {'a': 0, 'b': 1, 'c': 2, 'd': 0}})
        chain = [{"left": {"foo": "a"},
                  "center": "eq",
                  "right": {"foo": "b"}},
                 {"continue": "and"},
                 {"left": {'foo': 'c'},
                  "center": "gt",
                  "right": {'foo': 'b'}}]
        comp = Compare(chain=chain)
        comp.bindTo(state)
        self.assertFalse(comp.run())


if __name__ == "__main__":
    unittest.main()
