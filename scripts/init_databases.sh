#!/bin/bash
# Complete Database Initialization Script
# Initializes both PostgreSQL and MongoDB databases

set -e

echo "🚀 Starting complete database initialization..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${YELLOW}Project root: $PROJECT_ROOT${NC}"

# Initialize PostgreSQL
echo -e "\n${YELLOW}📊 Initializing PostgreSQL database...${NC}"
if command -v psql &> /dev/null; then
    # Run PostgreSQL init script
    "$SCRIPT_DIR/init_postgres.sh"
    echo -e "${GREEN}✅ PostgreSQL initialization completed${NC}"
else
    echo -e "${RED}❌ PostgreSQL client not found. Make sure PostgreSQL is installed.${NC}"
    echo -e "${YELLOW}💡 For Docker Compose, run: docker-compose exec postgres bash -c 'apt-get update && apt-get install -y postgresql-client'${NC}"
    exit 1
fi

# Initialize MongoDB
echo -e "\n${YELLOW}🍃 Initializing MongoDB databases...${NC}"
if command -v python3 &> /dev/null; then
    cd "$PROJECT_ROOT"
    python3 "$SCRIPT_DIR/init_mongodb.py"
    echo -e "${GREEN}✅ MongoDB initialization completed${NC}"
else
    echo -e "${RED}❌ Python3 not found. Please install Python 3.${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 All databases initialized successfully!${NC}"
echo -e "${YELLOW}📋 Summary:${NC}"
echo "  • PostgreSQL (userdb): users table created, demo user added"
echo "  • MongoDB (resourcedb): 8 sample resources added"
echo "  • MongoDB (reservationdb): ready for reservations"
echo -e "\n${YELLOW}🔐 Demo credentials:${NC}"
echo "  Username: demo"
echo "  Password: Demo123!"
echo "  Email: demo@example.com"

echo -e "\n${GREEN}🚀 Your reservation system is ready to use!${NC}"