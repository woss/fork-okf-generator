/// Core utility library providing math and text helpers.
pub mod math;

/// Computes the nth Fibonacci number iteratively.
///
/// Returns `None` if `n` is negative, otherwise `Some(u64)`.
pub fn fibonacci(n: i32) -> Option<u64> {
    if n < 0 {
        return None;
    }
    let n = n as usize;
    match n {
        0 => Some(0),
        1 => Some(1),
        _ => {
            let mut a = 0u64;
            let mut b = 1u64;
            for _ in 2..=n {
                let next = a.checked_add(b)?;
                a = b;
                b = next;
            }
            Some(b)
        }
    }
}

/// Parses a comma-separated string into a vector of trimmed, non-empty strings.
pub fn split_csv(line: &str) -> Vec<&str> {
    line.split(',')
        .map(|s| s.trim())
        .filter(|s| !s.is_empty())
        .collect()
}

/// A simple struct representing a 2D coordinate.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Point {
    pub x: f64,
    pub y: f64,
}

impl Point {
    /// Create a new `Point` at the given coordinates.
    pub fn new(x: f64, y: f64) -> Self {
        Point { x, y }
    }

    /// Compute the Euclidean distance to another point.
    pub fn distance_to(&self, other: &Point) -> f64 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        (dx * dx + dy * dy).sqrt()
    }

    /// Return the origin point (0.0, 0.0).
    pub fn origin() -> Self {
        Point { x: 0.0, y: 0.0 }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fibonacci() {
        assert_eq!(fibonacci(0), Some(0));
        assert_eq!(fibonacci(1), Some(1));
        assert_eq!(fibonacci(10), Some(55));
    }
}
