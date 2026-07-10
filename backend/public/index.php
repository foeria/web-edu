<?php

declare(strict_types=1);

require __DIR__ . '/../vendor/autoload.php';

use Throwable;
use WebEdu\Config\Config;
use WebEdu\Http\Response;
use WebEdu\Router\Router;

try {
    $configArray = require __DIR__ . '/../config/app.php';
    $config = new Config($configArray);
    $router = new Router($config);

    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
    $uri = $_SERVER['REQUEST_URI'] ?? '/';

    $router->dispatch($method, $uri);
} catch (Throwable $e) {
    error_log((string) $e);
    Response::json(['error' => 'Internal server error'], 500);
}
