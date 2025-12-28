#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

# build images (must match k8s/deployments/*.yaml image names)
docker build -t reservation-user-service:latest services/user-service
docker build -t reservation-resource-service:latest services/resource-service
docker build -t reservation-reservation-service:latest services/reservation-service
docker build -t reservation-notification-service:latest services/notification-service
docker build -t reservation-frontend:latest frontend
docker build -t reservation-db-init:latest -f scripts/db-init/Dockerfile .

echo "Built images successfully."