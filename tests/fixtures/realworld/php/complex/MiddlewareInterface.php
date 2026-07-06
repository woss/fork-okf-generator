<?php

namespace App\Middleware;

use Psr\Http\Message\RequestInterface;

/**
 * Middleware interface for the HTTP pipeline.
 */
interface MiddlewareInterface {
    public function process(RequestInterface $request, callable $next): mixed;
}
