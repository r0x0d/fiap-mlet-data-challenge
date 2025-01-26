# Makefile for News Prediction API

# Variables
DOCKER_COMPOSE = podman-compose
PYTHON = python3
PIP = pip3
STREAMLIT = streamlit
UVICORN = uvicorn

# Default target
all: help

# Help target
help:
	@echo "Available commands:"
	@echo "  make build             - Build Docker containers"
	@echo "  make up                - Start all services"
	@echo "  make down              - Stop and remove all containers"
	@echo "  make restart           - Restart all services"
	@echo "  make logs              - View container logs"
	@echo "  make train             - Train and log model using MLflow"
	@echo "  make test-api          - Run API tests"
	@echo "  make format            - Format code using black"
	@echo "  make lint              - Lint code using flake8"
	@echo "  make clean             - Clean up temporary files"
	@echo "  make monitor           - Open monitoring tools"
	@echo "  make local-run         - Run services locally without Docker"
	@echo "  make docker-shell      - Open shell in API container"
	@echo "  make requirements      - Generate/update requirements.txt"

# Docker commands
build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart: down up

logs:
	$(DOCKER_COMPOSE) logs -f

# Development commands
train:
	$(PYTHON) train_model.py

test-api:
	$(PYTHON) -m pytest tests/

format:
	$(PYTHON) -m black .

lint:
	$(PYTHON) -m flake8 .

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache

# Monitoring commands
monitor:
	@echo "Opening monitoring tools..."
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3000"
	@echo "MLflow: http://localhost:5000"

# Local development commands
local-run:
	$(UVICORN) app.main:app --reload & \
	$(STREAMLIT) run streamlit_app.py

docker-shell:
	$(DOCKER_COMPOSE) exec api /bin/bash

# Dependency management
requirements:
	$(PIP) freeze > requirements.txt

.PHONY: all help build up down restart logs train test-api format lint clean monitor local-run docker-shell requirements