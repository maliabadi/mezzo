from mezzo.gesture import Gesture
from mezzo.gesture.alteration import Alteration
from mezzo.state import MezzoState, MezzoPath, dotdict,
dotform, popleft, popright,
read_form_to_write, is_mezzo_type


class Iteration(Gesture):
    """
    Format:
        { "each" : {"object": "attribute"},
          "local" : {"object": "attribute"},
          "do" : [ { "type" : "gesture", "body" : "..." } ]
        }

    >>> state = MezzoState({'foo': {'baz': {'bar': [1,2,3]},
                                    'counter': 0,
                                    'adder': 3}})
    >>> each = {'foo': {'baz' : 'bar'}}
    >>> local = {'foo': 'index'}
    >>> alteration = Alteration(left={'foo': 'counter'},
                            center="pluseq",
                            right={'foo': 'adder'})
    >>> iteration = Iteration(each=each,
                          local=local,
                          do=[alteration])
    >>> alteration.bindTo(state)
    >>> iteration.bindTo(state)
    >>> iteration.run()
    >>> state.namespaces
    {'foo': {'counter': 9, 'baz': {'bar': [1, 2, 3]}, 'adder': 3}}
    """

    require = ['each', 'local', 'do']

    def __init__(self, **kwargs):
        super(Iteration, self).__init__('iteration', **kwargs)

    def run(self):
        itereach = state.getNameSpace(self.each)
        if not isinstance(itereach, list):
            raise ValueError('Invalid "each" argument for Iteration Gesture')
        for item in itereach:
            for gest in self.do:
                gest.run()

    def setindex(self, index=0):
        state.setNameSpace(read_form_to_write(self.local, index))

    def getindex(self):
        return state.getNameSpace(self.local)

    def increment(self):
        self.setindex(self.getindex() + 1)


if __name__ == "__main__":
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
    assert state.namespaces == {'foo': {'counter': 9,
                                        'baz': {'bar': [1, 2, 3]},
                                        'adder': 3}}
