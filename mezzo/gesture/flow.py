from mezzo.gesture import Gesture
from mezzo.gesture.comparison import Compare
from mezzo.state import MezzoState
from mezzo.gesture.alteration import Alteration


class Flow(Gesture):
    """
    Format:
        { "chain": [
        { "if": { "type": "comparison", "chain" : []},
          "do": [ { "type" : "gesture", "body" : "..." } ],
          "stop": false } ] }

    >>> state = MezzoState({'foo': {'a': 0,
                                'b': 1,
                                'c': 2,
                                'd': 0,
                                'baz': {'bar': 0},
                                'adder': 1}})
    >>> comparison = Compare(chain=[{"left": {"foo": "a"},
                                 "center": "eq",
                                 "right": {"foo": "d"}},
                                {"continue": "and"},
                                {"left": {'foo': 'c'},
                                 "center": "gt",
                                 "right": {'foo': 'b'}}])
    >>> alteration = Alteration(left={'foo': {'baz': 'bar'}},
                            center="pluseq",
                            right={'foo': 'adder'})
    >>> flowchain = [{'comparison': comparison,
                  'do': [alteration],
                  'stop': False}]
    >>> flow = Flow(chain=flowchain)
    >>> comparison.bindTo(state)
    >>> alteration.bindTo(state)
    >>> flow.bindTo(state)
    >>> flow.run()
    >>> state.namespaces
    {'foo': {'a': 0, 'c': 2, 'b': 1, 'd': 0,
             'baz': {'bar': 1}, 'adder': 1}}
    """

    require = ['chain', 'state']

    def __init__(self, **kwargs):
        super(Flow, self).__init__('flow', **kwargs)

    @property
    def steps(self):
        return map(lambda x: FlowStep(**x).bind(self.state), self.chain)

    def run(self):
        self.validate()
        for step in self.steps:
            step.run()
            if step.evaluation and not step.stop:
                break


class FlowStep(object):

    require = ['comparison', 'do', 'stop']

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def validate(self):
        for name in self.require:
            if not hasattr(self, name):
                raise ValueError

    def bind(self, state):
        self.state = state
        return self

    @property
    def evaluation(self):
        return self.comparison.run()

    def run(self):
        self.validate()
        for gest in self.do:
            if self.evaluation:
                gest.run()


if __name__ == "__main__":
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
    assert state.namespaces == {'foo': {'a': 0,
                                        'c': 2,
                                        'b': 1,
                                        'd': 0,
                                        'baz': {'bar': 1},
                                        'adder': 1}}
