"""
    double_it(x)

Double a number.
"""
function double_it(x::Int)::Int
    return x * 2
end

"""
    greet(name)

Return a greeting string.
"""
function greet(name::String)::String
    return "Hello, $name"
end

"""A 2D point."""
struct Point
    x::Float64
    y::Float64
end

"""A named entity."""
struct User
    id::Int
    name::String
end

"""Abstract animal type."""
abstract type Animal end

"""Pi constant."""
const PI = 3.14159
