#!/bin/bash

# Build script for all Docker images
echo "🏗️  Building Docker images for reservation system..."
echo "=================================================="

# Colors for output
RED='\033[0:31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base directory
BASE_DIR="/Users/sudeatesoglu/Desktop/Akademik/CMPE363/reservation-system"

# Function to build image
build_image() {
    local service=$1
    local dockerfile_path=$2
    local image_name=$3
    
    echo -e "${YELLOW}Building $service...${NC}"
    if docker build -t $image_name $dockerfile_path; then
        echo -e "${GREEN}✓ $service built successfully${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed to build $service${NC}"
        return 1
    fi
}

# Build backend services
echo ""
echo "Building backend services..."
build_image "User Service" "$BASE_DIR/services/user-service" "reservation-user-service:latest"
build_image "Resource Service" "$BASE_DIR/services/resource-service" "reservation-resource-service:latest"
build_image "Reservation Service" "$BASE_DIR/services/reservation-service" "reservation-reservation-service:latest"
build_image "Notification Service" "$BASE_DIR/services/notification-service" "reservation-notification-service:latest"

# Build frontend
echo ""
echo "Building frontend..."
build_image "Frontend" "$BASE_DIR/frontend" "reservation-frontend:latest"

# Summary
echo ""
echo "=================================================="
echo -e "${GREEN}✓ All images built successfully!${NC}"
echo ""
echo "Built images:"
docker images | grep reservation-

echo ""
echo "To deploy to Kubernetes, run:"
echo "  kubectl apply -f k8s/namespace.yaml"
echo "  kubectl apply -f k8s/databases/"
echo "  kubectl apply -f k8s/deployments/"
