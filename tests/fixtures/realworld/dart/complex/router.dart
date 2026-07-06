/// HTTP Router with middleware support.
class Router {
  final List<Route> _routes = [];
  final List<Middleware> _middleware = [];

  void get(String path, Function handler) {
    _routes.add(Route('GET', path, handler));
  }

  void post(String path, Function handler) {
    _routes.add(Route('POST', path, handler));
  }

  dynamic dispatch(String method, String path) {
    for (final route in _routes) {
      if (route.method == method && route.path == path) {
        return route.handler();
      }
    }
    throw Exception('404');
  }

  void use(Middleware mw) => _middleware.add(mw);
}

class Route {
  final String method;
  final String path;
  final Function handler;

  Route(this.method, this.path, this.handler);
}

mixin LoggerMixin {
  void log(String message) => print('[LOG] $message');
}

enum HttpMethod { get, post, put, delete, patch }

int multiply(int a, int b) => a * b;
