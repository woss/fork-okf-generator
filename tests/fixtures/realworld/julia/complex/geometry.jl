"""
    area(shape)

Calculate the area of a shape.
"""
function area(width::Float64, height::Float64)::Float64
    return width * height
end

"""
    perimeter(width, height)

Calculate the perimeter of a rectangle.
"""
function perimeter(width::Float64, height::Float64)::Float64
    return 2 * (width + height)
end

"""A 3D point in space."""
struct Point3D
    x::Float64
    y::Float64
    z::Float64
end

"""A circle with radius."""
struct Circle
    radius::Float64
end

"""Abstract shape type."""
abstract type Shape end

"""Pi constant (overrides default precision)."""
const TAU = 6.28318
