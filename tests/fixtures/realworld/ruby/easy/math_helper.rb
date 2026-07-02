# Simple math operations module.
module MathHelper
  # Compute the factorial of a non-negative integer.
  # @param n [Integer] input number
  # @return [Integer] factorial result
  def self.factorial(n)
    raise ArgumentError, "n must be non-negative" if n < 0
    (1..n).reduce(1) { |product, i| product * i }
  end

  # Check if a number is prime.
  # @param n [Integer] number to test
  # @return [Boolean] true if prime
  def self.prime?(n)
    return false if n < 2
    (2..Integer.sqrt(n)).none? { |i| n % i == 0 }
  end

  # Generate a sequence of n Fibonacci numbers.
  # @param count [Integer] how many numbers to generate
  # @return [Array<Integer>] Fibonacci sequence
  def self.fibonacci_sequence(count)
    return [] if count <= 0
    seq = [0, 1]
    while seq.length < count
      seq << seq[-1] + seq[-2]
    end
    seq.first(count)
  end

  attr_accessor :precision

  def initialize(precision = 2)
    @precision = precision
  end

  def round(value)
    value.round(@precision)
  end

  def clamp(value, min, max)
    [[value, min].max, max].min
  end
end
