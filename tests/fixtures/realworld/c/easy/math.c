#include "math.h"

int int_sqrt(int n) {
    if (n <= 0) return 0;
    int x = n;
    int y = (x + 1) / 2;
    while (y < x) {
        x = y;
        y = (x + n / x) / 2;
    }
    return x;
}

int int_abs(int n) {
    return n < 0 ? -n : n;
}

int int_clamp(int value, int low, int high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

int vector2i_dot(Vector2i a, Vector2i b) {
    return a.x * b.x + a.y * b.y;
}
