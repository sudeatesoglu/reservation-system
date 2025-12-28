SHELL := /bin/bash

NAMESPACE ?= reservation-system
TIMEOUT ?= 300s

.PHONY: build deploy ci cd up pf up-all access help

build:
	NAMESPACE=$(NAMESPACE) TIMEOUT=$(TIMEOUT) ./scripts/pipeline/build-images.sh

deploy:
	NAMESPACE=$(NAMESPACE) TIMEOUT=$(TIMEOUT) ./scripts/pipeline/deploy-k8s.sh

ci:
	NAMESPACE=$(NAMESPACE) TIMEOUT=$(TIMEOUT) OPEN_FRONTEND=0 ./scripts/pipeline/run-local-cicd.sh

cd:
	NAMESPACE=$(NAMESPACE) TIMEOUT=$(TIMEOUT) OPEN_FRONTEND=0 ./scripts/pipeline/deploy-k8s.sh

up:
	NAMESPACE=$(NAMESPACE) TIMEOUT=$(TIMEOUT) OPEN_FRONTEND=1 ./scripts/pipeline/run-local-cicd.sh

pf:
	NAMESPACE=$(NAMESPACE) ./scripts/pipeline/port-forward-all.sh

access:
	@echo "🚀 Reservation System - Default Access URLs (NodePort)"
	@echo "=================================================="
	@echo "Frontend:           http://localhost:30080"
	@echo "User API:           http://localhost:30000"
	@echo "Resource API:       http://localhost:31001"
	@echo "Reservation API:    http://localhost:31002"
	@echo "Notification API:   http://localhost:31003"
	@echo "Grafana:            http://localhost:30300 (admin/admin)"
	@echo "Prometheus:         http://localhost:30909"
	@echo "RabbitMQ AMQP:      http://localhost:30672"
	@echo "RabbitMQ Mgmt:      http://localhost:31672"
	@echo "MongoDB:            http://localhost:30017"
	@echo "PostgreSQL:         http://localhost:30432"
	@echo ""
	@echo "Note: All services are now NodePort by default - no port forwarding needed!"

help:
	@echo "Available targets:"
	@echo "  build     - Build all Docker images"
	@echo "  deploy    - Deploy to Kubernetes"
	@echo "  ci        - Build, deploy, and test (CI mode)"
	@echo "  up        - Full pipeline with frontend access"
	@echo "  pf        - Show default access URLs (no port forwarding needed)"
	@echo "  access    - Show all service access URLs"
	@echo "  help      - Show this help message"
	@echo "  de        - Delete the entire namespace"

de:
	kubectl delete namespace reservation-system

up-all: ci pf
