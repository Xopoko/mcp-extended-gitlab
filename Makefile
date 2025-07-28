.PHONY: help build up down logs shell clean restart status

# Default target
help:
	@echo "MCP Extended GitLab - Docker Commands"
	@echo "======================================"
	@echo "make build     - Build Docker image"
	@echo "make up        - Start containers in background"
	@echo "make down      - Stop and remove containers"
	@echo "make logs      - View container logs"
	@echo "make shell     - Open shell in running container"
	@echo "make clean     - Remove containers and images"
	@echo "make restart   - Restart containers"
	@echo "make status    - Show container status"

# Build Docker image
build:
	docker-compose build

# Start containers
up:
	docker-compose up -d

# Stop containers
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f mcp-gitlab

# Open shell in container
shell:
	docker exec -it mcp-extended-gitlab /bin/bash

# Clean up everything
clean:
	docker-compose down -v
	docker rmi mcp-extended-gitlab:latest || true

# Restart containers
restart:
	docker-compose restart

# Show status
status:
	docker-compose ps