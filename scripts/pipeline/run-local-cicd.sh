#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

NAMESPACE="${NAMESPACE:-reservation-system}"
TIMEOUT="${TIMEOUT:-300s}"
OPEN_FRONTEND="${OPEN_FRONTEND:-1}"  # set to 0 to skip port-forward

"$ROOT_DIR/scripts/pipeline/build-images.sh"

# Deploy + wait for readiness + db init job
NAMESPACE="$NAMESPACE" TIMEOUT="$TIMEOUT" "$ROOT_DIR/scripts/pipeline/deploy-k8s.sh"

# Basic smoke tests
NAMESPACE="$NAMESPACE" "$ROOT_DIR/scripts/pipeline/smoke-test.sh"

if [[ "$OPEN_FRONTEND" == "1" ]]; then
  echo "Opening frontend via port-forward: http://localhost:5174"
  exec kubectl port-forward -n "$NAMESPACE" svc/frontend 5174:80
else
  echo "Done (OPEN_FRONTEND=0)."
fi
