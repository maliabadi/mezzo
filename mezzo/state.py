def dotform(array):
    """
    Just a helper to reduce the number of times the hideous
    string join method is used.
    """
    return ".".join(array)


def popleft(key):
    return key.split('.', 1)

def is_mezzo_type(value):
    return isinstance(value, (basestring, int, bool, list))


class MezzoPath(object):
    """
    This is a utility class for handling dictionary-form
    references to value namespaces within a given MezzoState.
    They might be nested dictionaries, because they get deserialized
    from JSON that way. But none of the dictionaries will have more than one
    key-value pair in them, and only the inner-most dictionary will
    contain the declared value.
    """
    def __init__(self, pathdict):
        self.pathdict = pathdict
        self.chain = []
        self.assembleChain()

    def assembleChain(self, current=False):
        if not current:
            current = self.pathdict
        for key, value in current.items():
            self.chain.append(key)
            if isinstance(value, dict):
                self.assembleChain(current=value)
            elif isinstance(value, (basestring, int, bool, list)):
                self.chain.append(value)

    def dotForm(self):
        return dotform(self.chain)

    def objectChain(self):
        return self.chain[0:-1]

    def value(self):
        return self.chain[-1]


class dotdict(dict):
    """
    Thanks to Mike DeSimone on Stack Overflow
    """
    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError, 'expected dict'

    def __setitem__(self, key, value):
        if '.' in key:
            left, right = popleft(key)
            target = self.setdefault(left, dotdict())
            if not isinstance(target, dotdict):
                raise KeyError
            target[right] = value
        else:
            if isinstance(value, dict) and not isinstance(value, dotdict):
                value = dotdict(value)
            dict.__setitem__(self, key, value)

    def __getitem__(self, key):
        if '.' not in key:
            return dict.__getitem__(self, key)
        left, right = popleft(key)
        target = dict.__getitem__(self, left)
        if not isinstance(target, dotdict):
            raise KeyError
        return target[right]

    def __contains__(self, key):
        if '.' not in key:
            return dict.__contains__(self, key)
        left, right = popleft(key)
        target = dict.__getitem__(self, left)
        if not isinstance(target, dotdict):
            return False
        return right in target

    def setdefault(self, key, default):
        if key not in self:
            self[key] = default
        return self[key]

    __setattr__ = __setitem__
    __getattr__ = __getitem__


class MezzoState(object):

    def __init__(self, namespaces={}):
        self.namespaces = dotdict(namespaces)

    def getNameSpace(self, path):
        """
        >>> state = MezzoState({'foo': {'baz': 'bar'}})
        >>> state.getNameSpace({'foo': 'baz'})
        'bar'
        """
        address = MezzoPath(path).dotForm()
        return self.namespaces[address]

    def setNameSpace(self, path):
        """
        >>> state = MezzoState({'foo': 'bar'})
        >>> state.setNameSpace({'foo': {'baz' : 'value'}})
        >>> state.namespaces
        {'foo': 'bar', 'baz': {'value'}}
        """
        path = MezzoPath(path)
        verified = []
        for key in path.objectChain():
            verified.append(key)
            checkKey = dotform(verified)
            if checkKey not in self.namespaces:
                self.namespaces[checkKey] = dotdict({})
        self.namespaces[dotform(path.objectChain())] = path.value()

