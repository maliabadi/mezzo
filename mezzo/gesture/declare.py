from mezzo.gesture import Gesture

class Declaration(Gesture):

	require = ['namespace', 'state']

	def __init__(self, **kwargs):
		super(Declaration, self).__init__('declaration', **kwargs)

	def validate(self):
		for name in self.require:
			if not hasattr(self, name):
				raise ValueError("Declaration Gesture missing required argument: %s" % name)

	def run(self):
		self.validate()
		self.state.setNameSpace(self.namespace)