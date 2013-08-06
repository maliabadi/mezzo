from mezzo.gesture import Gesture
from mezzo.state import MezzoState, MezzoPath, dotdict, dotform, popleft, is_mezzo_type
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


def popright(path):
    return path.rsplit('.', 1)


def read_form_to_write(path, value):
    """
    >>> readpath = {'foo': {'baz': 'bar'}}
    >>> value = 1
    >>> read_form_to_write(readpath, value)
    {'foo': {'baz': {'bar' : 1}}
    """
    mp = MezzoPath(path)
    dd = dotdict(path)
    ddRoot, ddKey = popright(mp.dotForm())
    dd[ddRoot] = {ddKey : value}
    return dd


class Alteration(Gesture):
    """
    Format: 
        {"left" : { "some object": "attribute name"},
         "center" : "andeq", 
         "right" : 1 }


    >>> state = MezzoState({'foo': {'baz': {'bar': 0}}})
    >>> alteration = Alteration(left={'foo': {'baz': 'bar'}},
                                center="pluseq",
                                right=1)
    >>> alteration.run()
    >>> state.namespaces
    {'foo': {'baz': {'bar': 1}}}
    """

    require = ['left', 'center', 'right' 'state']

    def __init__(self, **kwargs):
        super(Alteration, self).__init__('alteration', **kwargs)

    def run(self):
        if not self.center in operator_map:
            raise ValueError('Invalid center argument "%s"' % self.center)
        readLeft = state.getNameSpace(self.left)
        if not is_mezzo_type(readLeft):
            raise ValueError('Invalid Left Path "%s"' % self.left)
        if not is_mezzo_type(self.right):
            raise ValueError('Invalid Right Argument "%s"' % self.right)
        sendRight = operator_map[self.center](readLeft, self.right)
        writePath = read_form_to_write(self.left, sendRight)
        state.setNameSpace(writePath)


if __name__ == '__main__':
    state = MezzoState({'foo': {'baz': {'bar': 0}}})
    alteration = Alteration(left={'foo': {'baz': 'bar'}},
                            center="pluseq",
                            right=1)
    alteration.bindTo(state)
    alteration.run()
    assert state.namespaces == {'foo': {'baz': {'bar': 1}}}
