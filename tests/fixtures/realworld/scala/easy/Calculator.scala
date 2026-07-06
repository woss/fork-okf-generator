/** A simple calculator. */
class Calculator {
  private var result: Int = 0

  def add(value: Int): Int = {
    result += value
    result
  }

  def getResult: Int = result
}

/** User account model. */
case class User(id: Int, name: String)

/** Service logger interface. */
trait Logger {
  def log(message: String): Unit
}

/** Application status. */
enum Status {
  case Active, Inactive, Banned
}

/** Top-level helper. */
def doubleIt(x: Int): Int = x * 2
