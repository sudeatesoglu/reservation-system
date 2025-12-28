#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-reservation-system}"

echo "All services are now configured as NodePort by default!"
echo "No manual port-forwarding required. Access services directly:"
echo ""

# Get the node IP (for Docker Desktop, this is typically localhost)
NODE_IP="${NODE_IP:-localhost}"

echo "Service Access URLs (NodePort):"
echo "================================="
echo "Frontend:           http://$NODE_IP:30080"
echo "User API:           http://$NODE_IP:30000"
echo "Resource API:       http://$NODE_IP:31001"
echo "Reservation API:    http://$NODE_IP:31002"
echo "Notification API:   http://$NODE_IP:31003"
echo "Grafana:            http://$NODE_IP:30300 (admin/admin)"
echo "Prometheus:         http://$NODE_IP:30909"
echo "RabbitMQ AMQP:      http://$NODE_IP:30672"
echo "RabbitMQ Mgmt:      http://$NODE_IP:31672"
echo "MongoDB:            http://$NODE_IP:30017"
echo "PostgreSQL:         http://$NODE_IP:30432"
echo ""

echo "Note: If running on Docker Desktop, use localhost as the IP."
echo "If running on a remote cluster, replace localhost with your node IP."

echo "Services are now accessible by default - no port forwarding required! 🎉"