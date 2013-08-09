$LOAD_PATH << File.dirname(File.dirname(__FILE__) + "/lib").to_s

module Mezzo
end

require 'mezzo/gesture'
require 'mezzo/state'
require 'mezzo/program'