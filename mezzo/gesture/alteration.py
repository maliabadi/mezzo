from mezzo.gesture import Gesture
from mezzo.state import MezzoState, MezzoPath, dotdict, dotform, popleft, popright, read_form_to_write, is_mezzo_type
from operator import iadd, iand, idiv, ilshift, imod, isub, irshift, isub, ior, isub, imul, ipow


operator_map = {"andeq" : iand,
                "oreq" : ior,
                "upbit" : irshift,
                "downbit" : ilshift, 
                "modeq" : imod,
                "diveq" : idiv,
                "multeq" : imul,
                "expeq" : ipow,
                "pluseq" :iadd,
                "minuseq": isub}


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

    require = ['left', 'center', 'right' 'state']

    def __init__(self, **kwargs):
        super(Alteration, self).__init__('alteration', **kwargs)

    def run(self):
        if not self.center in operator_map:
            raise ValueError('Invalid center argument "%s"' % self.center)
        readLeft = self.state.getNameSpace(self.left)
        readRight = self.state.getNameSpace(self.right)
        if not is_mezzo_type(readLeft):
            raise ValueError('Invalid Left Path "%s"' % self.left)
        if not is_mezzo_type(readRight):
            raise ValueError('Invalid Right Argument "%s"' % self.right)
        sendRight = operator_map[self.center](readLeft, readRight)
        writePath = read_form_to_write(self.left, sendRight)
        self.state.setNameSpace(writePath)


if __name__ == '__main__':
    state = MezzoState({'foo': {'baz': {'bar': 0}, 'adder': 4}})
    alteration = Alteration(left={'foo': {'baz': 'bar'}},
                            center="pluseq",
                            right={'foo': 'adder'})
    alteration.bindTo(state)
    alteration.run()
    assert state.namespaces == {'foo': {'baz': {'bar': 4}, 'adder': 4}}
