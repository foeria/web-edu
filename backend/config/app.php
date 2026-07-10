<?php

declare(strict_types=1);

return [
    'api_prefix' => '/api',
    'storage_path' => $_ENV['PHP_STORAGE_PATH'] ?? '/var/www/storage',
    'allowed_upload_types' => [
        'images' => ['jpg', 'jpeg', 'png', 'gif', 'webp'],
        'documents' => ['pdf', 'doc', 'docx', 'txt'],
    ],
];
