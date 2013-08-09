module Mezzo
	
	class ObjectStore

		attr :objects

		def initialize(objects={})
			@objects = objects
		end

		def hashify_namespace ns
		end

		def chainify_namespace ns
		end

	end

	class State

		attr :objects, :directives

		def initialize(objects={}, directives=[])
			@objects = objects
			@directives = directives
		end

		def get(ns)
			# TODO
		end

		def set(ns)
			# TODO
		end

		def build_path(ns)
			# TODO
		end

		def declare(params={})
			Gesture::Declaration.new(params)
				.attach(self)
				.run()
		end

		def alter(params={})
			Gesture::Alteration.new(params)
				.attach(self)
				.run()
		end

		def bind(params={})
			Gesture::Binding.new(params)
				.attach(self)
				.run()
		end

		def invoke(params={})
			Gesture::Invocation.new(params)
				.attach(self)
				.run()
		end

		def flow(params={})
			Gesture::Flow.new(params)
				.attach(self)
				.run()
		end

		def compare(params={})
			Gesture::Comparison.new(params)
				.attach(self)
				.run()
		end

		def iterate(params={})
			Gesture::Iteration.new(params)
				.attach(self)
				.run()
		end



	end

end