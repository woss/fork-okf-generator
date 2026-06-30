/// Math utilities for the application.
pub mod math {
    /// Adds two numbers together.
    pub fn add(a: i32, b: i32) -> i32 {
        a + b
    }

    /// Computes the factorial of n.
    pub fn factorial(n: u64) -> u64 {
        (1..=n).product()
    }
}

/// A simple counter that can be incremented.
pub struct Counter {
    value: i64,
}

impl Counter {
    /// Create a new Counter starting at 0.
    pub fn new() -> Self {
        Counter { value: 0 }
    }

    /// Increment the counter by 1.
    pub fn inc(&mut self) {
        self.value += 1;
    }

    /// Get the current count.
    pub fn get(&self) -> i64 {
        self.value
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(math::add(2, 3), 5);
    }
}
