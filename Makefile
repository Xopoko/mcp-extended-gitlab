.PHONY: help install dev test lint format clean build docker-build docker-run

# Default target
help:
	@echo "MCP Extended GitLab - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install    - Install package in editable mode"
	@echo "  make dev        - Install with development dependencies"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code with black"
	@echo "  make test       - Run tests"
	@echo "  make coverage   - Run tests with coverage"
	@echo ""
	@echo "Docker:"
	@echo "  make build      - Build Docker image"
	@echo "  make up         - Start Docker containers"
	@echo "  make down       - Stop Docker containers"
	@echo "  make logs       - View container logs"
	@echo ""
	@echo "Tools:"
	@echo "  make list-tools - List all available tools"
	@echo "  make stats      - Show project statistics"
	@echo "  make check-config - Check configuration"
	@echo ""
	@echo "Other:"
	@echo "  make clean      - Clean build artifacts"

# Installation
install:
	pip install -e .

dev:
	pip install -e ".[dev]"

# Code Quality
lint:
	@echo "Running ruff..."
	ruff check mcp_extended_gitlab/
	@echo "Running mypy..."
	mypy mcp_extended_gitlab/ --ignore-missing-imports || true

format:
	@echo "Formatting with black..."
	black mcp_extended_gitlab/

# Testing
test:
	pytest tests/ -v

test-unit:
	pytest tests/ -v -m unit

test-integration:
	pytest tests/ -v -m integration

coverage:
	pytest tests/ --cov=mcp_extended_gitlab --cov-report=html --cov-report=term

# Docker
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f mcp-gitlab

shell:
	docker exec -it mcp-extended-gitlab /bin/bash

status:
	docker-compose ps

# Development Tools
list-tools:
	python scripts/dev_tools.py list-tools

list-presets:
	python scripts/dev_tools.py list-presets

stats:
	python scripts/dev_tools.py stats --format detailed

check-config:
	python scripts/dev_tools.py config --check

test-tool:
	@echo "Usage: make test-tool TOOL=<tool_name> [PARAMS='{}']"
	@echo "Example: make test-tool TOOL=list_projects PARAMS='{\"per_page\": 5}'"
ifdef TOOL
	python scripts/test_tools.py $(TOOL) $(if $(PARAMS),--params '$(PARAMS)')
endif

# Running the server
run:
	python -m mcp_extended_gitlab

run-debug:
	python -m mcp_extended_gitlab --debug

run-minimal:
	GITLAB_ENABLED_TOOLS=minimal python -m mcp_extended_gitlab

run-filtered:
ifdef TOOLS
	GITLAB_ENABLED_TOOLS=$(TOOLS) python -m mcp_extended_gitlab
else
	@echo "Usage: make run-filtered TOOLS=<preset_or_tool_list>"
	@echo "Example: make run-filtered TOOLS=minimal"
	@echo "Example: make run-filtered TOOLS=list_projects,get_project"
endif

# Cleaning
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/

# Development environment
dev-env:
	@echo "Setting up development environment..."
	@echo "Creating .env file template..."
	@echo "GITLAB_PRIVATE_TOKEN=your_token_here" > .env.template
	@echo "GITLAB_BASE_URL=https://gitlab.com/api/v4" >> .env.template
	@echo "GITLAB_ENABLED_TOOLS=core" >> .env.template
	@echo "GITLAB_LOG_LEVEL=INFO" >> .env.template
	@echo ""
	@echo "Template created at .env.template"
	@echo "Copy to .env and update with your values"