#!/bin/bash

# Complete deployment script for Kubernetes
echo "Deploying Reservation System to Kubernetes..."
echo "=================================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

NAMESPACE="reservation-system"

# Step 1: Create namespace
echo -e "${YELLOW}Step 1: Creating namespace...${NC}"
kubectl apply -f k8s/namespace.yaml
sleep 2

# Step 2: Apply secrets and configmaps
echo -e "${YELLOW}Step 2: Applying secrets and configmaps...${NC}"
kubectl apply -f k8s/secrets/ 2>/dev/null || echo "Secrets already exist or not needed"
kubectl apply -f k8s/configmaps/ 2>/dev/null || echo "ConfigMaps already exist or not needed"
sleep 2

# Step 3: Create persistent volumes
echo -e "${YELLOW}Step 3: Creating persistent storage...${NC}"
kubectl apply -f k8s/storage/ 2>/dev/null || echo "Storage already exists"
sleep 3

# Step 4: Deploy databases
echo -e "${YELLOW}Step 4: Deploying databases...${NC}"
kubectl apply -f k8s/databases/
echo "Waiting for databases to be ready (60 seconds)..."
sleep 60

# Check database status
echo "Database pod status:"
kubectl get pods -n $NAMESPACE | grep -E "(postgres|mongo|rabbitmq)"

# Step 5: Deploy microservices
echo -e "${YELLOW}Step 5: Deploying microservices...${NC}"
kubectl apply -f k8s/deployments/
echo "Waiting for services to be ready (30 seconds)..."
sleep 30

# Step 6: Deploy monitoring
echo -e "${YELLOW}Step 6: Deploying monitoring...${NC}"
kubectl apply -f k8s/monitoring/
sleep 10

# Step 7: Apply ingress
echo -e "${YELLOW}Step 7: Applying ingress...${NC}"
kubectl apply -f k8s/ingress.yaml 2>/dev/null || echo "Ingress not configured or not needed"

# Final status
echo ""
echo "=================================================="
echo -e "${GREEN}Deployment complete!${NC}"
echo ""
echo "Checking pod status:"
kubectl get pods -n $NAMESPACE
echo ""
echo "Checking services:"
kubectl get svc -n $NAMESPACE
echo ""
echo "To access the application:"
echo "  Frontend: kubectl port-forward -n $NAMESPACE svc/frontend 5173:80"
echo "  Grafana:  kubectl port-forward -n $NAMESPACE svc/grafana 3000:3000"
echo ""
echo "Or access Grafana directly at: http://localhost:30300"
