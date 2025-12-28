#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

NAMESPACE="${NAMESPACE:-reservation-system}"
TIMEOUT="${TIMEOUT:-300s}"

kubectl apply -k k8s/

# Wait for core deployments
kubectl wait --for=condition=available deployment/user-service -n "$NAMESPACE" --timeout="$TIMEOUT"
kubectl wait --for=condition=available deployment/resource-service -n "$NAMESPACE" --timeout="$TIMEOUT"
kubectl wait --for=condition=available deployment/reservation-service -n "$NAMESPACE" --timeout="$TIMEOUT"
kubectl wait --for=condition=available deployment/notification-service -n "$NAMESPACE" --timeout="$TIMEOUT"
kubectl wait --for=condition=available deployment/frontend -n "$NAMESPACE" --timeout="$TIMEOUT"

# Wait for DB init job (if present)
if kubectl get job/db-init -n "$NAMESPACE" >/dev/null 2>&1; then
  kubectl wait --for=condition=complete job/db-init -n "$NAMESPACE" --timeout="$TIMEOUT"
fi

echo "Kubernetes deploy complete."