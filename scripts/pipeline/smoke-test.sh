#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-reservation-system}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-30}"

# Test services directly within the cluster using a temporary pod
TEST_POD_NAME="smoke-test-$(date +%s)"

cleanup() {
  kubectl delete pod "$TEST_POD_NAME" -n "$NAMESPACE" --ignore-not-found=true --timeout=10s >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "Running smoke tests in namespace '$NAMESPACE'..."

# Create a temporary pod for testing
kubectl run "$TEST_POD_NAME" \
  --image=curlimages/curl:latest \
  --restart=Never \
  --namespace="$NAMESPACE" \
  --command -- sleep 300 >/dev/null 2>&1

# Wait for pod to be ready
kubectl wait --for=condition=ready pod/"$TEST_POD_NAME" -n "$NAMESPACE" --timeout="${TIMEOUT_SECONDS}s" >/dev/null 2>&1

check_service() {
  local service_url="$1"
  local service_name="$2"

  echo "Testing $service_name..."
  if kubectl exec "$TEST_POD_NAME" -n "$NAMESPACE" -- \
     curl -f -s --max-time 10 "$service_url" >/dev/null 2>&1; then
    echo "  ✓ $service_name is healthy"
    return 0
  else
    echo "  ✗ $service_name failed" >&2
    return 1
  fi
}

# Test all services
check_service "http://user-service:8000/health" "User Service"
check_service "http://resource-service:8001/health" "Resource Service"
check_service "http://reservation-service:8002/health" "Reservation Service"
check_service "http://notification-service:8003/health" "Notification Service"
check_service "http://frontend:80/" "Frontend"

# Test that resources are seeded
echo "Testing resource seeding..."
if kubectl exec "$TEST_POD_NAME" -n "$NAMESPACE" -- \
   curl -f -s --max-time 10 "http://resource-service:8001/api/v1/resources" | grep -q '"name"' >/dev/null 2>&1; then
  echo "  ✓ Resources are seeded"
else
  echo "  ✗ Resource seeding failed" >&2
  exit 1
fi

echo ""
echo "All smoke tests passed! ✅"