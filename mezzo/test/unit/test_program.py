import unittest

from mezzo.program import MezzoProgram


class TestProgram(unittest.TestCase):

    def runTest(self):
        obj = {'objects': {'foo': {'adder': 1}},
               'directives': [{"type": "declaration",
                               "namespace": {'foo':
                                            {'baz': {'bar': 0}}}},
                              {"type": "binding",
                               "namespace": {'foo': 'myfunction'},
                               "arguments": {'argone': 1, 'argtwo': 2},
                               "locals": ['localone', 'localtwo'],
                               "body": [{'type': 'alteration',
                                         'left': {'foo': {'baz': 'bar'}},
                                         'center': 'pluseq',
                                         'right': {'foo': 'adder'}}]},
                              {"type": "invocation",
                               "namespace": {'foo': "myfunction"},
                               "arguments": {'argone': 2, 'argtwo': 2}}]}
        tar = {'foo': {'adder': 1,
               'baz': {'bar': 1},
               'myfunction': {'arguments': {'argone': False, 'argtwo': False},
                              'body': [{'center': 'pluseq',
                                        'left': {'foo': {'baz': 'bar'}},
                                        'right': {'foo': 'adder'}}],
                              'locals': {'localone': False,
                                         'localtwo': False}}}}
        prog = MezzoProgram(**obj)
        prog.run()
        self.assertEqual(prog.state.namespaces, tar)


if __name__ == "__main__":
    unittest.main()
