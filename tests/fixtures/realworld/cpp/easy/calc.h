#ifndef OKFGEN_CALC_H
#define OKFGEN_CALC_H

/// Namespace for basic arithmetic operations.
namespace okfgen {

    /// A simple calculator that maintains an internal accumulator.
    class Calculator {
    public:
        /// Construct a Calculator with an optional initial value.
        explicit Calculator(double initial = 0.0);

        /// Add a value to the accumulator.
        Calculator& add(double value);

        /// Subtract a value from the accumulator.
        Calculator& subtract(double value);

        /// Multiply the accumulator by a value.
        Calculator& multiply(double value);

        /// Divide the accumulator by a value.
        /// @throws std::invalid_argument if value is zero.
        Calculator& divide(double value);

        /// Return the current accumulator value.
        double value() const;

        /// Reset the accumulator to zero.
        void clear();

    private:
        double accumulator_;
    };

}  // namespace okfgen

#endif  // OKFGEN_CALC_H
