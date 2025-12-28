#!/bin/bash
# PostgreSQL Database Initialization Script
# This script is now handled by the db-init container using init_postgres.sql
# Kept for backward compatibility and manual execution

set -e

# Database connection details
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-userdb}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}

echo "Initializing PostgreSQL database: $DB_NAME"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is ready!"

# Run the SQL initialization
echo "Running database initialization..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$(dirname "$0")/init_postgres.sql"

echo "PostgreSQL database initialization completed successfully!"
echo "Demo user created: demo@example.com / Demo123!"