<?php

declare(strict_types=1);

namespace WebEdu\Storage;

use InvalidArgumentException;
use RuntimeException;
use WebEdu\Config\Config;

final class StorageService
{
    private Config $config;

    public function __construct(Config $config)
    {
        $this->config = $config;
    }

    public function storeUploadedFile(array $file, string $type): string
    {
        $this->validateUploadedFile($file);
        $this->validateTypeFolder($type);

        $extension = $this->extractExtension($file['name']);

        if (!$this->validateType($extension, $type)) {
            throw new InvalidArgumentException(
                sprintf('File type "%s" is not allowed for "%s" uploads.', $extension, $type)
            );
        }

        $this->validateMimeType($file['tmp_name'], $extension);

        $filename = $this->generateId($extension);
        $destinationPath = $this->buildDestinationPath($type, $filename);

        if (!move_uploaded_file($file['tmp_name'], $destinationPath)) {
            throw new RuntimeException('Failed to store uploaded file.');
        }

        return $type . '/' . $filename;
    }

    public function getUrl(string $id): string
    {
        return '/storage/' . $id;
    }

    private function validateType(string $extension, string $type): bool
    {
        $allowed = $this->config->get('allowed_upload_types.' . $type, []);

        return in_array(strtolower($extension), $allowed, true);
    }

    private function validateUploadedFile(array $file): void
    {
        if (!isset($file['error'], $file['tmp_name'], $file['name'])) {
            throw new InvalidArgumentException('Invalid uploaded file metadata.');
        }

        if ($file['error'] !== UPLOAD_ERR_OK) {
            throw new InvalidArgumentException($this->formatUploadError($file['error']));
        }

        if (!is_uploaded_file($file['tmp_name'])) {
            throw new InvalidArgumentException('Invalid or missing uploaded file.');
        }
    }

    private function formatUploadError(int $code): string
    {
        return match ($code) {
            UPLOAD_ERR_INI_SIZE => 'The uploaded file exceeds the server limit.',
            UPLOAD_ERR_FORM_SIZE => 'The uploaded file exceeds the form limit.',
            UPLOAD_ERR_PARTIAL => 'The uploaded file was only partially uploaded.',
            UPLOAD_ERR_NO_FILE => 'No file was uploaded.',
            UPLOAD_ERR_NO_TMP_DIR => 'Missing a temporary upload folder.',
            UPLOAD_ERR_CANT_WRITE => 'Failed to write uploaded file to disk.',
            UPLOAD_ERR_EXTENSION => 'A PHP extension stopped the file upload.',
            default => 'Unknown upload error.',
        };
    }

    private function validateTypeFolder(string $type): void
    {
        $allowedTypes = array_keys($this->config->get('allowed_upload_types', []));

        if (!in_array($type, $allowedTypes, true)) {
            throw new InvalidArgumentException(sprintf('Unknown upload type "%s".', $type));
        }
    }

    private function extractExtension(string $filename): string
    {
        $extension = pathinfo($filename, PATHINFO_EXTENSION);

        return strtolower($extension);
    }

    private function validateMimeType(string $tmpPath, string $extension): void
    {
        $finfo = new \finfo(FILEINFO_MIME_TYPE);
        $mimeType = $finfo->file($tmpPath);

        if ($mimeType === false) {
            throw new RuntimeException('Unable to determine file MIME type.');
        }

        $expectedMimes = $this->mimeMap()[$extension] ?? [];

        if (!in_array($mimeType, $expectedMimes, true)) {
            throw new InvalidArgumentException(
                sprintf('MIME type "%s" is not allowed for extension "%s".', $mimeType, $extension)
            );
        }
    }

    /**
     * @return array<string, list<string>>
     */
    private function mimeMap(): array
    {
        return [
            'jpg' => ['image/jpeg'],
            'jpeg' => ['image/jpeg'],
            'png' => ['image/png'],
            'gif' => ['image/gif'],
            'webp' => ['image/webp'],
            'pdf' => ['application/pdf'],
            'doc' => ['application/msword'],
            'docx' => ['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
            'txt' => ['text/plain'],
        ];
    }

    private function generateId(string $extension): string
    {
        return sprintf('%s.%s', bin2hex(random_bytes(16)), $extension);
    }

    private function buildDestinationPath(string $type, string $id): string
    {
        $basePath = rtrim($this->config->get('storage_path', '/var/www/storage'), '/');
        $directory = sprintf('%s/uploads/%s', $basePath, $type);

        if (!is_dir($directory) && !mkdir($directory, 0755, true) && !is_dir($directory)) {
            throw new RuntimeException(sprintf('Failed to create storage directory "%s".', $directory));
        }

        return $directory . '/' . $id;
    }
}
