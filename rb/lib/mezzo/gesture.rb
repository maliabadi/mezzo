module Mezzo
	module Gesture

		class GestureError < StandardError
		end

		class GestureBase
			
			@@required = [:state]

			def self.needs(*attributes)
				if attributes.is_a?(Array)
					@@required = attributes
				elsif attributes.is_a?(String) || attributes.is_a?(Symbol)
					@@required << attributes
				else
					raise ArgumentError
				end
			end

			def self.requirements
				@@required
			end

			attr :state

			def initialize(params={})
				params.each &method(:instance_variable_set)
			end

			def validate
				self.requirements.each do |req|
					raise GestureError "Missing required attribute #{req}" unless instance_variable_get(req)
				end
			end

			def attach(instance)
				@state = instance
			end


		end

		class Declaration < GestureBase
			needs :namespace
			
			def run
				validate
				state.
			end
		end

		class Alteration < GestureBase
			
			needs :left, :center, :right

			def run
				#TODO
			end
		end

		class Binding < GestureBase

			needs :namespace, :arguments, :locals, :body
			
			def run
				#TODO
			end
		end

		class Comparison < GestureBase

			needs :left, :center, :right
			
			def run
				#TODO
			end
		end

		class Flow < GestureBase

			needs :chain
			
			def run
				#TODO
			end
		end

		class Invocation < GestureBase

			needs :namespace, :arguments
			
			def run
				#TODO
			end
		end

		class Iteration < GestureBase

			needs :each, :local, :do
			
			def run
				#TODO
			end
		end

	end
end
