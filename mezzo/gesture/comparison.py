from mezzo.gesture import Gesture
from mezzo.state import is_mezzo_type, MezzoState
from operator import eq, ne, gt, lt, and_, or_, xor


def present(a,b):
  if isinstance(a, basestring, list):
    return len(a) > 0 and b
  if isinstance(a, int):
    return a > 0 and b
  if isinstance(a, bool):
    return a and b


def xand(a, b):
  return not all(a, b)


comparison_map = { "eq": eq,
                   "ne" : ne,
                   "lt" : lt,
                   "gt": gt, 
                   "is" : present }


relational_operators = { "and" : and_,
                         "or" : or_,
                         "xor" : xor,
                         "xand" : xand }

class Compare(Gesture):
    """
    Format: 
        { "chain": [ { "left": {"an object": {"a nested object": "attribute name"}}, 
                       "center": "eq",
                       "right": {"an object": {"a nested object": "attribute name"}}},
                     { "continue": "and" },
                     { "left": {"an object": {"a nested object": "attribute name"}}, 
                       "center": "lt",
                       "right": {"an object": {"a nested object": "attribute name"}}, 
                       "negate": "false" } ] }
    

    >>> state = MezzoState({'foo': {'a': 0, 'b': 1, 'c': 2, 'd': 0}})
    >>> chain = [ { "left": {'foo': 'a'}, 
                           "center": "eq",
                           "right": {'foo': 'd'}},
                         { "continue": "and" },
                         { "left": {'foo': 'c'}, 
                           "center": "gt",
                           "right": {'foo': 'b'}} ]
    >>> comp = Compare(chain=chain)
    >>> comp.bindTo(state)
    >>> comp.run()
    True

    >>> chain = [ { "left": {'foo': 'a'}, 
                          "center": "eq",
                          "right": {'foo': 'b'}},
                         { "continue": "and" },
                         { "left": {'foo': 'c'}, 
                           "center": "gt",
                           "right": {'foo': 'b'}} ]
    >>> comp = Compare(chain=chain)
    >>> comp.bindTo(state)
    >>> print comp.run()
    False

    """

    require = ['chain', 'state']

    def __init__(self, **kwargs):
        self.evalchain = []
        self.breakonfalse = False
        super(Compare, self).__init__('comparison', **kwargs)


    def last(self):
        return self.evalchain[-1]


    def run(self):
        self.validate()
        if not isinstance(self.chain, list):
            raise ValueError
        for link in self.chain:
            if not 'continue' in link:
                self.compareOne(link['left'], link['center'], link['right'])
                if self.breakonfalse and not self.last():
                    break
            else:
              if link['continue'] == 'and':
                  if not self.last():
                      break
                  else:
                      self.breakonfalse = True
              if link['continue'] == 'or':
                  self.breakonfalse = True
              if link['continue'] == 'xor':
                  if not self.last():
                      self.breakonfalse = False
                  else:
                      self.breakonfalse = True
              if link['continue'] == 'xand':
                  if not self.last():
                      self.breakonfalse = True
                  else:
                      self.breakonfalse = False
        return self.last()


    def compareOne(self, left, center, right):
        readLeft = state.getNameSpace(left)
        center = comparison_map[center]
        readRight = state.getNameSpace(right) 
        self.evalchain.append(center(readLeft, readRight))


if __name__ == "__main__":
    state = MezzoState({'foo': {'a': 0, 'b': 1, 'c': 2, 'd': 0}})
    chain = [ { "left": {'foo': 'a'}, 
                           "center": "eq",
                           "right": {'foo': 'd'}},
                         { "continue": "and" },
                         { "left": {'foo': 'c'}, 
                           "center": "gt",
                           "right": {'foo': 'b'}} ]
    comp = Compare(chain=chain)
    comp.bindTo(state)
    assert comp.run()
    chain = [ { "left": {'foo': 'a'}, 
                          "center": "eq",
                          "right": {'foo': 'b'}},
                         { "continue": "and" },
                         { "left": {'foo': 'c'}, 
                           "center": "gt",
                           "right": {'foo': 'b'}} ]
    comp = Compare(chain=chain)
    comp.bindTo(state)
    assert not comp.run()