#ifndef OKFGEN_MATH_H
#define OKFGEN_MATH_H

/** @brief Compute the integer square root using Newton's method. */
int int_sqrt(int n);

/** @brief Return the absolute value of an integer. */
int int_abs(int n);

/** @brief Clamp a value between low and high. */
int int_clamp(int value, int low, int high);

/** @brief A 2D vector with integer components. */
typedef struct {
    int x;
    int y;
} Vector2i;

/** @brief Compute the dot product of two 2D vectors. */
int vector2i_dot(Vector2i a, Vector2i b);

#endif /* OKFGEN_MATH_H */
