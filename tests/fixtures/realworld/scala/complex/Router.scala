/** HTTP Router with middleware support. */
class Router {
  private var routes: List[Route] = List.empty

  def add(method: String, path: String, handler: () => Any): Unit = {
    routes = routes :+ Route(method, path, handler)
  }

  def dispatch(method: String, path: String): Option[Any] = {
    routes.find(r => r.method == method && r.path == path).map(_.handler())
  }
}

case class Route(method: String, path: String, handler: () => Any)

/** Logging middleware trait. */
trait Logging {
  def log(message: String): Unit = println(s"[LOG] $message")
}

/** Response status codes. */
enum StatusCode {
  case Ok, NotFound, InternalServerError
}

/** Top-level helper. */
def add(x: Int, y: Int): Int = x + y
