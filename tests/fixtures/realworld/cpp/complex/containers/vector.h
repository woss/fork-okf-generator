#ifndef OKFGEN_VECTOR_H
#define OKFGEN_VECTOR_H

#include <cstddef>
#include <stdexcept>

namespace okfgen {

/// A minimal dynamic array (vector) implementation.
template <typename T>
class Vector {
public:
    /// Construct an empty vector.
    Vector() noexcept;

    /// Construct a vector with count default-inserted elements.
    explicit Vector(std::size_t count);

    /// Copy constructor.
    Vector(const Vector& other);

    /// Copy assignment operator.
    Vector& operator=(const Vector& other);

    /// Destructor.
    ~Vector() noexcept;

    /// Add an element to the end.
    void push_back(const T& value);

    /// Remove the last element.
    /// @throws std::out_of_range if the vector is empty.
    void pop_back();

    /// Access element at index with bounds checking.
    const T& at(std::size_t index) const;

    /// Access element at index (no bounds checking).
    const T& operator[](std::size_t index) const;

    /// Return the number of elements.
    std::size_t size() const noexcept;

    /// Return whether the vector is empty.
    bool empty() const noexcept;

    /// Remove all elements.
    void clear() noexcept;

    /// Reserve capacity for at least new_cap elements.
    void reserve(std::size_t new_cap);

    /// Return the current capacity.
    std::size_t capacity() const noexcept;

private:
    T* data_;
    std::size_t size_;
    std::size_t capacity_;

    static constexpr std::size_t kInitialCapacity = 4;

    void reallocate(std::size_t new_cap);
};

}  // namespace okfgen

#include "vector.cpp"
#endif  // OKFGEN_VECTOR_H
