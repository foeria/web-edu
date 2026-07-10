<?php

declare(strict_types=1);

namespace WebEdu\Router;

use InvalidArgumentException;
use RuntimeException;
use WebEdu\Config\Config;
use WebEdu\Http\Response;
use WebEdu\Storage\StorageService;

final class Router
{
    private Config $config;
    private StorageService $storage;

    public function __construct(Config $config)
    {
        $this->config = $config;
        $this->storage = new StorageService($config);
    }

    public function dispatch(string $method, string $uri): never
    {
        $path = $this->normalizePath($uri);
        $prefix = $this->config->get('api_prefix', '/api');

        if (!str_starts_with($path, $prefix)) {
            Response::json(['error' => 'not found'], 404);
        }

        $route = substr($path, strlen($prefix)) ?: '/';

        return match (true) {
            $method === 'GET' && $route === '/health' => $this->health(),
            $method === 'POST' && $route === '/upload' => $this->upload(),
            $method === 'GET' && str_starts_with($route, '/files/') => $this->filePlaceholder($route),
            default => Response::json(['error' => 'not found'], 404),
        };
    }

    private function normalizePath(string $uri): string
    {
        $withoutQuery = explode('?', $uri, 2)[0];

        return $withoutQuery === '' ? '/' : $withoutQuery;
    }

    private function health(): never
    {
        Response::json(['status' => 'ok']);
    }

    private function upload(): never
    {
        if (!isset($_FILES['file'])) {
            Response::json(['error' => 'No file provided.'], 400);
        }

        $type = $_POST['type'] ?? 'images';

        try {
            $id = $this->storage->storeUploadedFile($_FILES['file'], $type);
            $url = $this->storage->getUrl($id);
            $size = $_FILES['file']['size'] ?? 0;

            Response::json([
                'id' => $id,
                'url' => $url,
                'type' => $type,
                'size' => $size,
            ]);
        } catch (InvalidArgumentException $e) {
            Response::json(['error' => $e->getMessage()], 400);
        } catch (RuntimeException $e) {
            Response::json(['error' => $e->getMessage()], 500);
        }
    }

    private function filePlaceholder(string $route): never
    {
        $id = substr($route, strlen('/files/'));

        if ($id === '' || $id === false) {
            Response::json(['error' => 'not found'], 404);
        }

        Response::json([
            'message' => 'file metadata placeholder',
            'id' => $id,
        ]);
    }
}
