#include "vector.h"
#include <algorithm>

namespace okfgen {

template <typename T>
Vector<T>::Vector() noexcept
    : data_(nullptr), size_(0), capacity_(0) {}

template <typename T>
Vector<T>::Vector(std::size_t count)
    : data_(new T[count]), size_(count), capacity_(count) {
    for (std::size_t i = 0; i < count; ++i) {
        data_[i] = T();
    }
}

template <typename T>
Vector<T>::Vector(const Vector& other)
    : data_(new T[other.capacity_]), size_(other.size_), capacity_(other.capacity_) {
    for (std::size_t i = 0; i < size_; ++i) {
        data_[i] = other.data_[i];
    }
}

template <typename T>
Vector<T>& Vector<T>::operator=(const Vector& other) {
    if (this != &other) {
        Vector tmp(other);
        std::swap(data_, tmp.data_);
        std::swap(size_, tmp.size_);
        std::swap(capacity_, tmp.capacity_);
    }
    return *this;
}

template <typename T>
Vector<T>::~Vector() noexcept {
    delete[] data_;
}

template <typename T>
void Vector<T>::push_back(const T& value) {
    if (size_ == capacity_) {
        reallocate(capacity_ == 0 ? kInitialCapacity : capacity_ * 2);
    }
    data_[size_++] = value;
}

template <typename T>
void Vector<T>::pop_back() {
    if (empty()) {
        throw std::out_of_range("pop_back on empty Vector");
    }
    --size_;
}

template <typename T>
const T& Vector<T>::at(std::size_t index) const {
    if (index >= size_) {
        throw std::out_of_range("Vector index out of range");
    }
    return data_[index];
}

template <typename T>
const T& Vector<T>::operator[](std::size_t index) const {
    return data_[index];
}

template <typename T>
std::size_t Vector<T>::size() const noexcept {
    return size_;
}

template <typename T>
bool Vector<T>::empty() const noexcept {
    return size_ == 0;
}

template <typename T>
void Vector<T>::clear() noexcept {
    size_ = 0;
}

template <typename T>
void Vector<T>::reserve(std::size_t new_cap) {
    if (new_cap > capacity_) {
        reallocate(new_cap);
    }
}

template <typename T>
std::size_t Vector<T>::capacity() const noexcept {
    return capacity_;
}

template <typename T>
void Vector<T>::reallocate(std::size_t new_cap) {
    T* new_data = new T[new_cap];
    for (std::size_t i = 0; i < size_; ++i) {
        new_data[i] = data_[i];
    }
    delete[] data_;
    data_ = new_data;
    capacity_ = new_cap;
}

}  // namespace okfgen
