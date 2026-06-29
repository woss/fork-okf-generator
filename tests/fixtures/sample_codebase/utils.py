"""Utility functions for sample codebase."""

def add(a: int, b: int) -> int:
    """Add two integers together."""
    return a + b

def greet(name: str) -> str:
    """Return a greeting string."""
    return f"Hello, {name}!"

class Calculator:
    """A simple calculator class."""

    def __init__(self):
        self.history = []

    def add(self, a: int, b: int) -> int:
        """Add two numbers and record result."""
        result = a + b
        self.history.append(result)
        return result

    def reset(self):
        """Clear calculation history."""
        self.history = []
