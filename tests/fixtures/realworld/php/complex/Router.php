<?php

namespace App\Routing;

use Psr\Http\Message\RequestInterface;
use App\Middleware\MiddlewareInterface;

/**
 * HTTP Router with middleware support.
 */
class Router {
    private array $routes = [];
    private array $middleware = [];

    public function addRoute(string $method, string $path, callable $handler, array $middleware = []): void {
        $this->routes[] = [
            'method' => $method,
            'path' => $path,
            'handler' => $handler,
            'middleware' => $middleware,
        ];
    }

    public function dispatch(RequestInterface $request): mixed {
        foreach ($this->routes as $route) {
            if ($route['method'] === $request->getMethod() && $route['path'] === $request->getUri()) {
                $chain = $this->buildMiddlewareChain($route);
                return $chain($request);
            }
        }
        throw new \RuntimeException('No matching route', 404);
    }

    private function buildMiddlewareChain(array $route): callable {
        $handler = $route['handler'];
        foreach (array_reverse(array_merge($this->middleware, $route['middleware'])) as $mw) {
            $handler = fn($req) => $mw->process($req, $handler);
        }
        return $handler;
    }

    public function addMiddleware(MiddlewareInterface $mw): void {
        $this->middleware[] = $mw;
    }
}
