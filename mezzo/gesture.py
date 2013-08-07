import operator as op
from mezzo.state import *


gestures = ['declaration', 'alteration', 'iteration',
            'flow', 'comparison', 'binding', 'invocation']


def present(a, b):
    if isinstance(a, basestring, list):
        return len(a) > 0 and b
    if isinstance(a, int):
        return a > 0 and b
    if isinstance(a, bool):
        return a and b


def xand(a, b):
    return not all(a,  b)


operator_map = {"andeq": op.iand,
                "oreq": op.ior,
                "upbit": op.irshift,
                "downbit": op.ilshift,
                "modeq": op.imod,
                "diveq": op.idiv,
                "multeq": op.imul,
                "expeq": op.ipow,
                "pluseq": op.iadd,
                "minuseq": op.isub,
                "eq": op.eq,
                "ne": op.ne,
                "lt": op.lt,
                "gt": op.gt,
                "is": present,
                "and": op.and_,
                "or": op.or_,
                "xor": op.xor,
                "xand": xand}


class Gesture(object):
    """
    Base Gesture class and the list of supported gesture types
    """

    require = []

    def __init__(self, kind, **kwargs):
        if not kind in gestures:
            raise ValueError("Gesture Type '%s' not supported" % kind)
        self.kind = kind
        for key, value in kwargs.items():
            setattr(self, key, value)

    def bindTo(self, state):
        if not isinstance(state, MezzoState):
            raise ValueError("Cannot bind gesture non-MezzoState object")
        self.state = state

    def validate(self):
        for name in self.require:
            if not hasattr(self, name):
                raise ValueError

    def serialize(self):
        struct = {'type': self.kind}
        for name in self.require:
            if name != 'state':
                struct[name] = getattr(self, name)
        return struct


class Alteration(Gesture):
    """
    Format:
        {"left" : { "some object": "attribute name"},
         "center" : "andeq",
         "right" : 1 }


    >>> state = MezzoState({'foo': {'baz': {'bar': 0}, 'adder': 4}})
    >>> alteration = Alteration(left={'foo': {'baz': 'bar'}},
                                center="pluseq",
                                right={'foo': 'adder'})
    >>> alteration.run()
    >>> state.namespaces
    {'foo': {'baz': {'bar': 4}, 'adder': 4}}
    """

    require = ['left', 'center', 'right', 'state']

    def __init__(self, **kwargs):
        super(Alteration, self).__init__('alteration', **kwargs)

    @property
    def readLeft(self):
        return self.state.getNameSpace(self.left)

    @property
    def readRight(self):
        return self.state.getNameSpace(self.right)

    @property
    def sendRight(self):
        return operator_map[self.center](self.readLeft,
                                         self.readRight)

    def send(self):
        self.state.setNameSpace(read_form_to_write(self.left,
                                                   self.sendRight))

    def run(self):
        if not self.center in operator_map:
            raise ValueError('Invalid center argument "%s"' % self.center)
        if not is_mezzo_type(self.readLeft):
            raise ValueError('Invalid Left Path "%s"' % self.left)
        if not is_mezzo_type(self.readRight):
            raise ValueError('Invalid Right Argument "%s"' % self.right)
        self.send()


class Binding(Gesture):
    """
    Format:
        { "namespace": {"an object": {"a nested object": "attribute name"}},
          "arguments": { "a named argument" : "default value",
                         "a named argument" : "default value" },
          "locals" : [ "attribute name", "attibute name", "attribute name"],
          "body" : [ { "type" : "gesture", "body": "..." } ] }
    """

    require = ['namespace', 'arguments', 'locals', 'body', 'state']

    def __init__(self, **kwargs):
        super(Binding, self).__init__('binding', **kwargs)

    def run(self):
        self.validate()
        self.loadReferences()
        self.register()

    def register(self):
        self.registerArguments()
        self.registerLocals()
        self.registerBody()

    def loadReferences(self):
        self.asdot = dotdict(self.namespace)
        self.mp = MezzoPath(self.asdot)
        self.objchain = dotform(self.mp.objectChain())

    def registerArguments(self):
        for key, value in self.arguments.items():
            self.asdot[self.objchain] = {self.mp.value(): {'arguments': key}}
            self.state.setNameSpace(read_form_to_write(self.asdot, value))

    def registerLocals(self):
        for name in self.locals:
            self.asdot[self.objchain] = {self.mp.value(): {'locals': name}}
            self.state.setNameSpace(read_form_to_write(self.asdot, False))

    def registerBody(self):
        self.asdot[self.objchain] = {self.mp.value(): 'body'}
        self.state.setNameSpace(read_form_to_write(self.asdot, self.body))


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
        itereach = self.state.getNameSpace(self.each)
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


class Declaration(Gesture):
    """
    Format:
        { "namespace":
            { "some object": { "attribute name" : "value" } } }
    """
    require = ['namespace', 'state']

    def __init__(self, **kwargs):
        super(Declaration, self).__init__('declaration', **kwargs)

    def run(self):
        self.validate()
        self.state.setNameSpace(self.namespace)


class Compare(Gesture):
    """
    Format:
        { "chain": [ { "left":
                            {"an object":
                                {"a nested object": "attribute name"}},
                       "center": "eq",
                            {"an object":
                                {"a nested object": "attribute name"}},
                     { "continue": "and" } ] }

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
    >>> comp.run()
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
        readLeft = self.state.getNameSpace(left)
        center = operator_map[center]
        readRight = self.state.getNameSpace(right)
        self.evalchain.append(center(readLeft, readRight))

key_to_class = {'declaration': Declaration,
                'alteration': Alteration,
                'iteration': Iteration,
                'flow': Flow,
                'comparison': Compare,
                'binding': Binding,
                'invocation': Invocation}
