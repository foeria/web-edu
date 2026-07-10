<?php

declare(strict_types=1);

namespace WebEdu\Config;

final class Config
{
    /** @var array<string, mixed> */
    private array $values;

    public function __construct(array $values)
    {
        $this->values = $values;
    }

    public function get(string $key, mixed $default = null): mixed
    {
        $keys = explode('.', $key);
        $value = $this->values;

        foreach ($keys as $segment) {
            if (!is_array($value) || !array_key_exists($segment, $value)) {
                return $default;
            }

            $value = $value[$segment];
        }

        return $value;
    }
}
