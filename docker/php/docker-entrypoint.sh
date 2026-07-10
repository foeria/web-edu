#!/bin/sh
set -e

# Ensure the local storage mount is writable by the php-fpm worker.
chown -R www-data:www-data /var/www/storage 2>/dev/null || true

exec "$@"
