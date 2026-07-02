#include "calc.h"
#include <stdexcept>

namespace okfgen {

Calculator::Calculator(double initial)
    : accumulator_(initial) {}

Calculator& Calculator::add(double value) {
    accumulator_ += value;
    return *this;
}

Calculator& Calculator::subtract(double value) {
    accumulator_ -= value;
    return *this;
}

Calculator& Calculator::multiply(double value) {
    accumulator_ *= value;
    return *this;
}

Calculator& Calculator::divide(double value) {
    if (value == 0.0) {
        throw std::invalid_argument("Division by zero");
    }
    accumulator_ /= value;
    return *this;
}

double Calculator::value() const {
    return accumulator_;
}

void Calculator::clear() {
    accumulator_ = 0.0;
}

}  // namespace okfgen
