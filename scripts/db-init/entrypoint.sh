#!/bin/sh
set -eu

POSTGRES_HOST="${POSTGRES_HOST:-postgres}"
POSTGRES_DB="${POSTGRES_DB:-userdb}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-postgres}"

MONGO_HOST="${MONGO_HOST:-mongodb}"
MONGO_PORT="${MONGO_PORT:-27017}"

export PGPASSWORD="$POSTGRES_PASSWORD"

echo "Waiting for PostgreSQL at ${POSTGRES_HOST}:5432..."
until pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER" >/dev/null 2>&1; do
  sleep 2
done

echo "Running PostgreSQL init SQL..."
psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /app/init_postgres.sql

echo "Waiting for MongoDB at ${MONGO_HOST}:${MONGO_PORT}..."
python3 - <<'PY'
import os, time
from pymongo import MongoClient
host=os.getenv('MONGO_HOST','mongodb')
port=int(os.getenv('MONGO_PORT','27017'))
for _ in range(120):
    try:
        c=MongoClient(f"mongodb://{host}:{port}/", serverSelectionTimeoutMS=1000)
        c.admin.command('ping')
        print('MongoDB is ready')
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit('MongoDB not reachable')
PY

echo "Running MongoDB init script..."
MONGO_HOST="$MONGO_HOST" MONGO_PORT="$MONGO_PORT" python3 /app/init_mongodb.py

echo "DB initialization finished."
