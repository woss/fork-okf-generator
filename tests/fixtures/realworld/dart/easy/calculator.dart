/// A simple calculator.
class Calculator {
  int result = 0;

  Calculator(this.result);

  /// Add a value to the result.
  int add(int value) => result += value;

  int subtract(int value) => result -= value;

  static String version() => '1.0.0';
}

/// User account model.
class User {
  final int id;
  final String name;

  User(this.id, this.name);

  String greet() => 'Hi $name';
}

/// Application status.
enum Status { active, inactive, banned }

/// Top-level helper function.
int doubleIt(int x) => x * 2;
