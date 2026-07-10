<?php

declare(strict_types=1);

namespace WebEdu\Http;

final class Response
{
    public static function json(mixed $data, int $status = 200): never
    {
        http_response_code($status);
        header('Content-Type: application/json; charset=utf-8');

        $encoded = json_encode($data, JSON_THROW_ON_ERROR);

        echo $encoded;
        exit;
    }
}
