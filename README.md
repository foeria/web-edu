# Web-Edu

A Nuxt 4 frontend with a lightweight PHP 8.2 backend served behind Nginx.

## Setup

1. Install frontend dependencies and generate the static build:

   ```bash
   cd nuxt-app
   pnpm install
   pnpm generate
   cd ..
   ```

2. Install PHP dependencies (for local development / IDE):

   ```bash
   cd backend
   composer install
   cd ..
   ```

3. Copy environment files and adjust as needed:

   ```bash
   cp .env.example .env
   cp nuxt-app/.env.example nuxt-app/.env
   ```

4. Build and start the Docker services:

   ```bash
   docker compose -f docker/docker-compose.yml up --build -d
   ```

5. Verify the backend health endpoint:

   ```bash
   curl http://localhost/api/health
   ```

   Expected response:

   ```json
   { "status": "ok" }
   ```

## Project Layout

- `nuxt-app/` — Nuxt 4 frontend (kept intact)
- `backend/` — PHP backend source code
- `docker/` — Nginx and PHP-FPM Docker images
- `storage/` — Local uploads, cache, and logs

## Notes

- The `storage/` directory must be writable by the PHP-FPM worker (`www-data`).
- The `php-vendor` named volume preserves Composer dependencies installed inside the Docker image.
