# Library Management System

Flask + MySQL Library Management System running with Docker Compose.

## Requirements

- Docker Desktop
- Git

## One-shot local run

1. Start from a clean database:

```bash
docker compose down -v --remove-orphans
docker compose up --build
```

3. Open:

`http://localhost:5000`

The SQL file in `db/lms.sql` initializes the database automatically on the first start of a fresh MySQL volume.

## Docker Hub

```bash
docker pull rahulsingh2k/library-management-system:latest
docker compose pull
docker compose up
```

## Stop

```bash
docker compose down
```

## Reset database

```bash
docker compose down -v --remove-orphans
docker compose up --build
```

> `down -v` deletes the MySQL data volume.

## Health check

`http://localhost:5000/health`
