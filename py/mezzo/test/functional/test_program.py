import json
from os import getcwd
from mezzo.program import deserialize, MezzoProgram
from pprint import pprint


def testProgram():
    with open("%s/test_one.json" % getcwd(), 'r') as file:
        program = deserialize(file.read())
    program.run()
    function = {u'arguments': {u'argone': False,
                               u'argtwo': False},
                u'body': [{u'center': u'pluseq',
                           u'left': {u'foo': {u'baz': u'bar'}},
                           u'right': {u'foo': u'adder'}}],
                u'locals': {u'localone': False,
                            u'localtwo': False}}
    tar = {u'foo': {u'adder': 1,
                    u'baz': {u'bar': 1},
                    u'myfunction': function}}
    assert program.state.namespaces == tar


if __name__ == "__main__":
    testProgram()
